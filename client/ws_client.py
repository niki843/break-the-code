#!/usr/bin/env python

import asyncio
import json

import websockets


# Initial connection to server throw exception if an error occurs
async def connect_to_server():
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            await websocket.send(json.dumps({"type": "new_game"}))
            msg = await websocket.recv()
            print(msg)
    except ConnectionRefusedError:
        print("Could not connect to server")
    except Exception as e:
        print("An unknown exception occurred")


if __name__ == "__main__":
    asyncio.run(connect_to_server())
