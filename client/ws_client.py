import json

import websockets
import pygame


# Initial connection to server throw exception if an error occurs
from websockets.exceptions import ConnectionClosed

IPADDRESS = "localhost"
PORT = "8765"

EVENT_TYPE = pygame.event.custom_type()


class WebsocketClient:
    def __init__(self):
        self.websocket = None

    async def connect_to_server(self):
        try:
            async with websockets.connect(f"ws://{IPADDRESS}:{PORT}") as websocket:
                self.websocket = websocket
                print("Connected to server")
                await self.wait_for_server_message()
        except ConnectionRefusedError:
            print("Could not connect to server")

    async def wait_for_server_message(self):
        if not self.websocket:
            raise Exception("No active connection!")
        async for message in self.websocket:
            print(f"[Received]: {message}")
            message = json.loads(message)
            if message.get("type") == "connection_closed":
                await self.websocket.close()
                return
            pygame.fastevent.post(pygame.event.Event(EVENT_TYPE, message=message))

    async def send_server_messages(self, message):
        print("SENDING MESSAGE")
        await self.websocket.send(message)
        print("Message sent")
