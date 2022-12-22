#!/usr/bin/env python

import asyncio
import websockets
import json
import uuid

from websockets.exceptions import ConnectionClosed

from entity.game_session import GameSession
from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull

# key: id of the game session
# value: ids of the players so they can rejoin
from utils.enums import GameState

GAME_SESSIONS = {}

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
            websocket=websocket
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

    await receive_user_input(websocket, current_game_session)


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

    await receive_user_input(websocket, current_game_session)


async def send_message(websocket, message_type, message, **kwargs):
    event = {
        "type": message_type,
        "message": message,
    }
    event.update(kwargs)
    await websocket.send(json.dumps(event))


async def receive_user_input(websocket, game_session):
    while True:
        try:
            await websocket.recv()
        except ConnectionClosed:
            # If the game has ended, delete the game session from the dict
            if game_session.get_state() == GameState.END:
                del GAME_SESSIONS[game_session.id]
                return

            print("Waiting for player to reconnect")
            return


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
            await websocket.send(json.dumps(GAME_SESSIONS.keys()))

    if event_msg.get("type") == "join_game":
        await join_game(
            websocket, event_msg.get("game_session_id"), event_msg.get("player_id"), event_msg.get("player_name")
        )

    if event_msg.get("type") == "new_game":
        await create_game(websocket, event_msg.get("player_id"), event_msg.get("player_name"))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
