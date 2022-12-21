#!/usr/bin/env python

import asyncio
import websockets
import json
import uuid

from entity.game_session import GameSession
from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull

# key: id of the game session
# value: ids of the players so they can rejoin
GAME_SESSIONS = {}


async def create_game(websocket, player_id):
    started_game_session_id = str(uuid.uuid4())

    try:
        GAME_SESSIONS[started_game_session_id] = GameSession(
            session_id=started_game_session_id,
            host=str(player_id),
            websocket=websocket
        )
    except InvalidPlayerId:
        await send_message(
            websocket,
            message_type="error",
            message="The player id that was provided is not valid",
            error_type="player_id_not_valid",
        )

    await send_message(
        websocket,
        message_type="success",
        message="Successfully created a new game session.",
        game_session_id=started_game_session_id,
    )

    async for message in websocket:
        print(message)


async def join_game(websocket, game_session_id, player_id):
    if game_session_id not in GAME_SESSIONS.keys():
        await send_message(
            websocket,
            message_type="error",
            message="This game session could not be found!",
            error_type="session_not_found",
        )

    current_game_session = GAME_SESSIONS[game_session_id]

    try:
        current_game_session.join_player(player_id, websocket)
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

    # Notify players of new player joining
    await current_game_session.send_joined_message(player_id)


async def send_message(websocket, message_type, message, **kwargs):
    event = {
        "type": message_type,
        "message": message,
    }
    event.update(kwargs)
    await websocket.send(json.dumps(event))


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
            websocket, event_msg.get("game_session_id"), event_msg.get("player_id")
        )

    if event_msg.get("type") == "new_game":
        await create_game(websocket, event_msg.get("player_id"))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
