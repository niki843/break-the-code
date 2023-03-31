#!/usr/bin/env python

import asyncio

import websockets
import json
import uuid

from websockets.exceptions import ConnectionClosed

from server.custom_exceptions.incorrect_amount_of_cards_in_guess import (
    IncorrectAmountOfCardsInGuess,
)
from server.custom_exceptions.incorrect_card import IncorrectCardPlayed
from server.custom_exceptions.incorrect_card_number_input import (
    IncorrectCardNumberInput,
)
from server.custom_exceptions.incorrect_number_card_value import (
    IncorrectNumberCardValue,
)
from server.custom_exceptions.not_your_turn import NotYourTurn
from server.service.game_session import GameSession
from server.custom_exceptions.invalid_id import InvalidPlayerId
from server.custom_exceptions.session_full import SessionFull

from server.utils.enums import GameState, PlayerStatus

# key: id of the game session
# value: ids of the players so they can rejoin
GAME_SESSIONS = {}

# Can be used to send message to all players
CURRENT_WEBSOCKET_CONNECTIONS = []

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
    except InvalidPlayerId:
        await send_message(
            websocket,
            message_type="error",
            message="The player id that was provided is not valid",
            error_type="player_id_not_valid",
        )

    GAME_SESSIONS[started_game_session_id] = current_game_session

    await send_message(
        websocket,
        message_type="success",
        message="Successfully created a new game session.",
        game_session_id=started_game_session_id,
    )

    await handle_user_input(player_id, websocket, current_game_session)


async def join_game(websocket, game_session_id, player_id, player_name):
    if game_session_id not in GAME_SESSIONS.keys():
        await send_message(
            websocket,
            message_type="error",
            message="This game session could not be found!",
            error_type="session_not_found",
        )

    current_game_session = GAME_SESSIONS[game_session_id]

    try:
        await current_game_session.join_player(player_id, player_name, websocket)
    except SessionFull:
        await send_message(
            websocket,
            message_type="error",
            message="The game session is full",
            error_type="session_full",
        )
    except InvalidPlayerId:
        await send_message(
            websocket,
            message_type="error",
            message="The player id that was provided is not valid",
            error_type="player_id_not_valid",
        )

    # Notify all players of new player joining
    await current_game_session.send_joined_message(player_id, player_name)

    await handle_user_input(player_id, websocket, current_game_session)


async def handle_user_input(player_id, websocket, game_session):
    # TODO: Create a endpoint that will close the handle_user_input function
    #  like when a user exits the game or doesn't start the game session
    #  if it's the host this should again trigger the change host functionality
    while True:
        if game_session.get_state() == GameState.END:
            return

        try:
            msg = json.loads(await websocket.recv())
            msg_type = msg.get("type")

            # When we receive a close connection request
            # we send a message confirming a close the connection
            # then on the msg = json.loads(await websocket.recv()) we receive a
            # ConnectionClosed exception which is handled
            if msg_type == "close_connection":
                await send_message_and_close_connection(websocket)
                continue

            if game_session.get_player_by_id(player_id).is_eliminated:
                await send_message(
                    websocket,
                    message_type="player_eliminated",
                    message="You are eliminated and can't play anymore",
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
                    msg.get("condition_card_id"),
                    msg.get("card_number_choice", None),
                )
            elif (
                msg_type == "guess_numbers"
                and game_session.get_state() != GameState.END
            ):
                await validate_and_guess_numbers(
                    websocket,
                    player_id,
                    game_session,
                    msg.get("player_guess"),
                )
            elif msg_type == "chat_message":
                await game_session.send_message_to_all_others(
                    player_id, msg.get("content", None)
                )
            else:
                await send_message(
                    websocket=websocket,
                    message_type="incorrect_input",
                    message=f"Incorrect input type for the state {msg_type}",
                )

            # end the game session and delete it from list
            if game_session.get_state() == GameState.END:
                GAME_SESSIONS.pop(game_session.id, None)
                return

        except ConnectionClosed:
            # If the game has ended or all players are disconnected, delete the game session from the dict
            if (
                game_session.get_state() == GameState.END
                or game_session.are_all_players_disconnected()
            ):
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
                game_session.get_current_player().is_eliminated = True
                game_session.remove_player(player_id)
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


async def validate_and_start_game(websocket, player_id, game_session):
    if not player_id == game_session.get_host().id:
        await send_message(
            websocket,
            message_type="error",
            message="Only the host can start the game",
            error_type="insufficient_permissions",
        )
        return
    if not game_session.get_state() == GameState.PENDING:
        await send_message(
            websocket,
            message_type="error",
            message="The game can not be started from the current state",
            error_type="game_state_error",
        )
        return
    if game_session.get_players_count() < 3:
        await send_message(
            websocket,
            message_type="error",
            message="The game can not be started with less than 3 players",
            error_type="game_state_error",
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
    except NotYourTurn:
        await send_message(
            websocket,
            message_type="error",
            message="It's not your turn!",
            error_type="not_your_turn",
        )
    except IncorrectCardPlayed:
        await send_message(
            websocket,
            message_type="error",
            message="The card you requested is not in the current drawn cards",
            error_type="incorrect_card_player",
        )
    except IncorrectCardNumberInput:
        await send_message(
            websocket,
            message_type="error",
            message="The card number you provided is not accepted by the card condition",
            error_type="incorrect_card_number_input",
        )


async def validate_and_guess_numbers(websocket, player_id, game_session, player_guess):
    try:
        await game_session.guess_number_and_change_player(player_id, player_guess)
    except IncorrectNumberCardValue as e:
        await send_message(
            websocket,
            message_type="error",
            message="Incorrect number of cards",
            error_type="incorrect_number_card_value",
        )
    except IncorrectAmountOfCardsInGuess as e:
        await send_message(
            websocket,
            message_type="error",
            message="Incorrect amount of cards",
            error_type="incorrect_amount_of_cards",
        )
    except NotYourTurn as e:
        await send_message(
            websocket,
            message_type="error",
            message="It's not your turn!",
            error_type="not_your_turn",
        )


async def send_message_and_close_connection(websocket):
    await send_message(
        websocket,
        message_type="connection_closed",
        message="Closing the current connection",
    )
    await websocket.close()
    print("CLOSED CONNECTION")


# Handles all new incoming requests and distributes to appropriate functions
async def handler(websocket):
    # message = await websocket.recv()
    event_msg = None
    event_msg_type = None
    CURRENT_WEBSOCKET_CONNECTIONS.append(websocket)

    async for message in websocket:
        event_msg = json.loads(message)
        event_msg_type = event_msg.get("type")
        if (
            event_msg_type == "join_game"
            or event_msg_type == "new_game"
            or event_msg_type == "close_connection"
        ):
            break

        if event_msg_type == "end_session":
            return

        if event_msg_type == "get_current_games":
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

    # TODO: Make sure that when exiting join_game and new_game
    #  the connection is kept alive and we can still call get_current_games
    if event_msg and event_msg_type == "join_game":
        print("JOINING GAME")
        await join_game(
            websocket,
            event_msg.get("game_session_id"),
            event_msg.get("player_id"),
            event_msg.get("player_name"),
        )

    if event_msg and event_msg_type == "new_game":
        print("NEW GAME CREATION")
        await create_game(
            websocket, event_msg.get("player_id"), event_msg.get("player_name"), event_msg.get("room_name"),
        )

    if event_msg and event_msg_type == "close_connection":
        await send_message_and_close_connection(websocket)
        return


async def main():
    print("STARTING SERVER")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever
    print("CLOSING SERVER")


if __name__ == "__main__":
    asyncio.run(main())
