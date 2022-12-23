#!/usr/bin/env python

import asyncio
import aioconsole

import websockets


# Initial connection to server throw exception if an error occurs
from websockets.exceptions import ConnectionClosed


async def connect_to_server():
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            await asyncio.gather(wait_for_server_message(websocket), send_server_message(websocket))

    except ConnectionRefusedError:
        print("Could not connect to server")
    except Exception:
        print("An unknown exception occurred")


async def wait_for_server_message(websocket):
    async for message in websocket:
        try:
            print(message)
        except ConnectionClosed:
            print("The server closed the connection")


async def send_server_message(websocket):
    inp = await aioconsole.ainput('json: ')
    while inp != "end":
        await websocket.send(inp)
        inp = await aioconsole.ainput('json: ')


if __name__ == "__main__":
    asyncio.run(connect_to_server())
