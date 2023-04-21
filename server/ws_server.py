import asyncio
from json import JSONDecodeError

import websockets
import json
import uuid
import server
import custom_exceptions

from websockets.exceptions import ConnectionClosed

from server.custom_exceptions.game_excpetion import GameException
from server.service.game_session import GameSession

from server.utils.enums import GameState, PlayerStatus

# key: id of the game session
# value: ids of the players so they can rejoin
GAME_SESSIONS = {}

# Can be used to send message to all players
CURRENT_WEBSOCKET_CONNECTIONS = []

# Waiting for join_game clients
CLIENT_JOIN_GAME_QUEUE = []


# This will keep the player id of disconnected players
# mapped to game session ids
CLOSED_CONNECTION_PLAYER_ID_TO_GAME_SESSION_ID = {}


async def create_game(websocket, player_id, player_name, room_name):
    started_game_session_id = str(uuid.uuid4())
    current_game_session = None

    try:
        current_game_session = GameSession(
            session_id=started_game_session_id,
            player_id=player_id,
            player_name=player_name,
            websocket=websocket,
            room_name=room_name,
        )
    except custom_exceptions.InvalidPlayerIdException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )

    GAME_SESSIONS[started_game_session_id] = current_game_session

    await send_message(
        websocket,
        message_type=server.GAME_CREATED_MESSAGE_TYPE,
        message=server.GAME_SESSION_CREATED_MESSAGE,
        game_session_id=started_game_session_id
    )
    broadcast_message(
        CLIENT_JOIN_GAME_QUEUE,
        message_type=server.GAME_CREATED_MESSAGE_TYPE,
        message=server.GAME_SESSION_CREATED_MESSAGE,
        game_session_id=started_game_session_id,
        game_session_name=room_name,
        host_id=player_id,
        host_name=player_name
    )

    await handle_user_input(player_id, websocket, current_game_session)


async def join_game(websocket, game_session_id, player_id, player_name):
    if game_session_id not in GAME_SESSIONS.keys():
        await send_message(
            websocket,
            message_type=server.ERROR_MESSAGE_TYPE,
            message=server.GAME_SESSION_NOT_FOUND_MESSAGE,
            error_type=server.ERROR_TYPE_SESSION_NOT_FOUND,
        )

    current_game_session = GAME_SESSIONS[game_session_id]

    try:
        await current_game_session.join_player(player_id, player_name, websocket)
    except custom_exceptions.SessionFullException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )
    except custom_exceptions.InvalidPlayerIdException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )

    # Notify all players of new player joining
    await current_game_session.send_joined_message(player_id, player_name)
    broadcast_message(
        CLIENT_JOIN_GAME_QUEUE,
        message_type=server.PLAYER_JOINED_MESSAGE_TYPE,
        message=server.PLAYER_JOINED_MESSAGE,
        game_session_id=game_session_id,
        player_id=player_id,
        player_name=player_name,
    )

    await handle_user_input(player_id, websocket, current_game_session)


async def handle_user_input(player_id, websocket, game_session):
    while True:
        if game_session.get_state() == GameState.END:
            return

        try:
            msg_deserialized = await decode_json_and_send_message(await websocket.recv(), websocket)

            if not msg_deserialized:
                continue

            msg_type = msg_deserialized.get("type")

            # When we receive a close connection request
            # we send a message confirming a close the connection
            # then on the msg = json.loads(await websocket.recv()) we receive a
            # ConnectionClosed exception which is handled
            if msg_type == "close_connection":
                await send_message_and_close_connection(websocket)
                continue
            elif msg_type == "exit_game":
                raise custom_exceptions.PlayerLeftTheGameException(player_id)

            if game_session.get_player_by_id(player_id).is_eliminated:
                await send_message(
                    websocket,
                    message_type=server.PLAYER_ELIMINATED_MESSAGE_TYPE,
                    message=server.PLAYER_ELIMINATED_MESSAGE,
                )
                continue

            if msg_type == "start_game" and game_session.get_state() not in (
                GameState.END_ALL_CARDS_PLAYED,
                GameState.END,
            ):
                await validate_and_start_game(websocket, player_id, game_session)
            elif msg_type == "play_tile" and game_session.get_state() not in (
                GameState.END_ALL_CARDS_PLAYED,
                GameState.END,
            ):
                await validate_and_play_condition_card_request(
                    websocket,
                    player_id,
                    game_session,
                    msg_deserialized.get("condition_card_id"),
                    msg_deserialized.get("card_number_choice", None),
                )
            elif (
                msg_type == "guess_numbers"
                and game_session.get_state() != GameState.END
            ):
                await validate_and_guess_numbers(
                    websocket,
                    player_id,
                    game_session,
                    msg_deserialized.get("player_guess"),
                )
            elif msg_type == "chat_message":
                await game_session.send_message_to_all_others(
                    player_id, msg_deserialized.get("content", None)
                )
            else:
                await send_message(
                    websocket=websocket,
                    message_type=server.INCORRECT_INPUT_MESSAGE_TYPE,
                    message=server.INCORRECT_TYPE_MESSAGE,
                )

            # end the game session and delete it from list
            if game_session.get_state() == GameState.END:
                GAME_SESSIONS.pop(game_session.id, None)
                return

        except (ConnectionClosed, custom_exceptions.PlayerLeftTheGameException) as e:
            # If the game has ended or all players are disconnected, delete the game session from the dict
            if (
                game_session.get_state() == GameState.END
                or game_session.are_all_players_disconnected()
            ):
                if GAME_SESSIONS.get(game_session.id):
                    broadcast_message(
                        CLIENT_JOIN_GAME_QUEUE,
                        message_type=GameSession.GAME_SESSION_CLOSED_MESSAGE_TYPE,
                        message=GameSession.GAME_SESSION_CLOSED_WHEN_PENDING_MESSAGE,
                        game_session_id=game_session.id,
                        player_id=player_id
                    )
                    del GAME_SESSIONS[game_session.id]
                return

            if (
                player_id == game_session.get_host().get_id()
                and game_session.get_state() == GameState.PENDING
            ):
                game_session.replace_host(player_id)
                return

            game_session.player_disconnected_broadcast(player_id)

            game_session.set_player_disconnected(player_id)

            # If the game has not started we don't need to wait for re-connection
            if game_session.get_state() != GameState.IN_PROGRESS:
                game_session.remove_player(player_id)
                if not game_session.get_state() in (GameState.END, GameState.END_ALL_CARDS_PLAYED):
                    broadcast_message(
                        CLIENT_JOIN_GAME_QUEUE,
                        message_type="player_removed",
                        message="Player removed",
                        game_session_id=game_session.id,
                        player_id=player_id,
                    )
                return

            if not isinstance(e, custom_exceptions.PlayerLeftTheGameException):
                print(f"Waiting 30 seconds for player {player_id} to reconnect.")
                await asyncio.sleep(30)

            if (
                game_session.get_player_status_by_id(player_id)
                == PlayerStatus.DISCONNECTED
            ):
                print("Player did not re-connect")
                if game_session.have_all_players_disconnected():
                    print("All players disconnected deleting session")
                    del GAME_SESSIONS[game_session.id]
                    return

                game_session.player_not_reconnect_broadcast(player_id)
                game_session.get_player_by_id(player_id).is_eliminated = True
                if game_session.get_current_player().get_id() == player_id:
                    game_session.next_player()
                return
            else:
                game_session.player_reconnected_broadcast(player_id)
                print("Player re-connected")
                return


async def send_message(websocket, message_type, message, **kwargs):
    event = {
        "type": message_type,
        "message": message,
    }
    event.update(kwargs)
    await websocket.send(json.dumps(event))


def broadcast_message(websocket_connections, message_type, message, **kwargs):
    if not websocket_connections:
        return

    event = {
        "type": message_type,
        "message": message,
    }
    event.update(kwargs)
    websockets.broadcast(websocket_connections, json.dumps(event))


async def validate_and_start_game(websocket, player_id, game_session):
    if not player_id == game_session.get_host().id:
        await send_message(
            websocket,
            message_type=server.ERROR_MESSAGE_TYPE,
            message=server.ONLY_HOST_CAN_START_MESSAGE,
            error_type=server.ERROR_TYPE_INSUFFICIENT_PERMISSION,
        )
        return
    if not game_session.get_state() == GameState.PENDING:
        await send_message(
            websocket,
            message_type=server.ERROR_MESSAGE_TYPE,
            message=server.GAME_STARTING_FROM_WRONG_STATE_MESSAGE,
            error_type=server.ERROR_TYPE_GAME_STATE,
        )
        return
    if game_session.get_players_count() < 3:
        await send_message(
            websocket,
            message_type=server.ERROR_MESSAGE_TYPE,
            message=server.NOT_ENOUGH_PLAYERS_MESSAGE,
            error_type=server.ERROR_TYPE_GAME_STATE,
        )
        return

    await game_session.start_game()


# The validation will be happening in the game session and game board
# there is no validation that the server can do without too much information
# transfer up the line
async def validate_and_play_condition_card_request(
    websocket, player_id, game_session, condition_card_id, card_number_choice
):
    try:
        await game_session.play_condition_card_and_change_player(
            player_id, condition_card_id, card_number_choice
        )
    except custom_exceptions.NotYourTurnException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )
    except custom_exceptions.CardNotDrawnException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )
    except custom_exceptions.IncorrectConditionCardAdditionalInputException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )


async def validate_and_guess_numbers(websocket, player_id, game_session, player_guess):
    try:
        await game_session.guess_number_and_change_player(player_id, player_guess)
    except custom_exceptions.IncorrectNumberCardValueException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )
    except custom_exceptions.IncorrectAmountOfCardsInGuessException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )
    except custom_exceptions.NotYourTurnException as ex:
        await send_message(
            websocket,
            message_type=ex.name,
            message=ex.message,
            error_type=ex.error_type,
        )


async def send_message_and_close_connection(websocket):
    await send_message(
        websocket,
        message_type=server.CONNECTION_CLOSED_MESSAGE_TYPE,
        message=server.CONNECTION_CLOSED_MESSAGE,
    )
    await websocket.close()
    print("CLOSED CONNECTION")


async def decode_json_and_send_message(message, websocket):
    try:
        event_msg = json.loads(message)
    except JSONDecodeError:
        await send_message(
            websocket,
            message_type=GameException.NAME,
            message=server.JSON_DECODE_ERROR_MESSAGE,
            error_type=server.ERROR_TYPE_INCORRECT_JSON_FORMAT,
        )
        return
    return event_msg


def remove_player_from_join_game_queue(websocket):
    # Remove the player from the join game queue
    try:
        CLIENT_JOIN_GAME_QUEUE.remove(websocket)
    except ValueError:
        pass


# Handles all new incoming requests and distributes to appropriate functions
async def handler(websocket):
    CURRENT_WEBSOCKET_CONNECTIONS.append(websocket)

    async for message in websocket:
        event_msg = await decode_json_and_send_message(message, websocket)

        if not event_msg:
            continue

        event_msg_type = event_msg.get("type")

        match event_msg_type:
            case "get_current_games":
                # Add player to join_game_queue and send all updates until he joins a game
                CLIENT_JOIN_GAME_QUEUE.append(websocket)

                # Send all the current games to the player
                game_sessions = {}
                for game_session in GAME_SESSIONS.values():
                    if game_session.get_state() == GameState.PENDING:
                        game_sessions[game_session.id] = {
                                    "room_name": game_session.get_room_name(),
                                    "connected_players": game_session.get_players_count(),
                                    "player_id_name_map": game_session.get_player_id_name_map()
                                }
                print("SENDING OUT GAME SESSIONS")
                await send_message(
                    websocket,
                    "send_game_sessions",
                    "Sending out game sessions",
                    game_sessions=game_sessions,
                )
                continue
            case "exit_get_current_games":
                remove_player_from_join_game_queue(websocket)
            case "join_game":
                remove_player_from_join_game_queue(websocket)
                print("JOINING GAME")
                await join_game(
                    websocket,
                    event_msg.get("game_session_id"),
                    event_msg.get("player_id"),
                    event_msg.get("player_name"),
                )
                continue
            case "new_game":
                remove_player_from_join_game_queue(websocket)
                print("NEW GAME CREATION")
                await create_game(
                    websocket, event_msg.get("player_id"), event_msg.get("player_name"), event_msg.get("room_name"),
                )
                continue
            case "close_connection":
                remove_player_from_join_game_queue(websocket)
                await send_message_and_close_connection(websocket)
                return


async def main():
    print("STARTING SERVER")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever
    print("CLOSING SERVER")


if __name__ == "__main__":
    asyncio.run(main())
