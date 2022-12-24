#!/usr/bin/env python

import asyncio
import websockets
import json
import uuid

from websockets.exceptions import ConnectionClosed

from exceptions.incorrect_card import IncorrectCardPlayed
from exceptions.not_your_turn import NotYourTurn
from service.game_session import GameSession
from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull

from utils.enums import GameState

# key: id of the game session
# value: ids of the players so they can rejoin
GAME_SESSIONS = {}

# TODO: Add all live websocket connections
#  for sending messages to all players
CURRENT_WEBSOCKET_CONNECTIONS = []

# This will keep the player id of disconnected players
# mapped to game session ids
CLOSED_CONNECTION_PLAYER_ID_TO_GAME_SESSION_ID = {}


async def create_game(websocket, player_id, player_name):
    started_game_session_id = str(uuid.uuid4())
    current_game_session = None

    try:
        current_game_session = GameSession(
            session_id=started_game_session_id,
            player_id=player_id,
            player_name=player_name,
            websocket=websocket,
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
        current_game_session.join_player(player_id, player_name, websocket)
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
    await current_game_session.send_joined_message(player_id)

    await handle_user_input(player_id, websocket, current_game_session)


async def handle_user_input(player_id, websocket, game_session):
    while True:
        try:
            msg = json.loads(await websocket.recv())

            if msg.get("type") == "start_game":
                await validate_and_start_game(websocket, player_id, game_session)
            elif msg.get("type") == "play_tile":
                await validate_and_play_condition_card_request(
                    websocket, player_id, game_session, msg.get("condition_card_id")
                )
            elif msg.get("type") == "guess_numbers":
                await validate_and_guess_number(
                    websocket,
                    player_id,
                    game_session,
                    json.loads(msg.get("player_guess")),
                )

        except ConnectionClosed:
            # If the game has ended, delete the game session from the dict
            if game_session.get_state() == GameState.END:
                del GAME_SESSIONS[game_session.id]
                return

            # TODO: Implement reconnecting
            print("Waiting for player to reconnect")
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
    websocket, player_id, game_session, condition_card_id
):
    try:
        await game_session.play_condition_card_and_change_player(
            player_id, condition_card_id
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


async def validate_and_guess_number(websocket, player_id, game_session, player_guess):
    pass


# Handles all new incoming requests and distributes to appropriate functions
async def handler(websocket):
    # message = await websocket.recv()
    event_msg = None

    async for message in websocket:
        event_msg = json.loads(message)
        if event_msg.get("type") == "join_game" or event_msg.get("type") == "new_game":
            break

        if event_msg.get("type") == "end_session":
            return

        if event_msg.get("type") == "get_current_games":
            await websocket.send(
                json.dumps({"game_session_ids": list(GAME_SESSIONS.keys())})
            )

    if event_msg.get("type") == "join_game":
        await join_game(
            websocket,
            event_msg.get("game_session_id"),
            event_msg.get("player_id"),
            event_msg.get("player_name"),
        )

    if event_msg.get("type") == "new_game":
        await create_game(
            websocket, event_msg.get("player_id"), event_msg.get("player_name")
        )


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
