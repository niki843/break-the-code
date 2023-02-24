import uuid

import pygame
import os
import asyncio
from client import ws_client as client

img_path = f".{os.path.sep}images{os.path.sep}"
loop = asyncio.get_event_loop()

ws_client = client.WebsocketClient()


async def connect():
    print("Connecting to server")
    await ws_client.connect_to_server()
    print("Connected to server")


async def send_message(message):
    await ws_client.send_server_messages(message)

    print("Message sent")


def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()


# Connect to server
loop.create_task(connect())


def get_or_generate_player_id():
    # Open the player_id file or create it if not existing
    # and read the uuid or created if missing
    with open("player_id.txt", "a+") as f:
        if os.stat("player_id.txt").st_size == 0:
            f.write(str(uuid.uuid4()))

    # Open the player_id file and read the uuid
    f = open("player_id.txt", "r")
    player_id = f.read()
    return player_id


def start_game():
    player_id = get_or_generate_player_id()

    pygame.init()
    pygame.fastevent.init()
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Break The Code")
    thumbnail = pygame.image.load(
        f"{img_path}crack-the-code-thumbnail.png"
    )
    pygame.display.set_icon(thumbnail)

    background = pygame.image.load(f"{img_path}background.png")
    # set up the drawing window
    screen.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))
    pygame.display.flip()
    running = True
    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                loop.create_task(send_message('{"type": "close_connection"}'))
                running = False
            elif e.type == client.EVENT_TYPE:
                print(e.message)
            elif e.type == pygame.KEYUP and e.key == pygame.K_n:
                loop.create_task(send_message('{"type": "new_game", "player_id": "0ed61f48-2761-4c82-9460-788af1f52795", "player_name": "first_player"}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_c:
                loop.create_task(send_message('{"type": "get_current_games"}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_j:
                loop.create_task(send_message('{"type": "get_current_games"}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_j:
                loop.create_task(send_message('{"type": "get_current_games"}'))

        # tell event loop to run once
        # if there are no i/o events, this might return right away
        # if there are events or tasks that don't need to wait for i/o, then
        # run ONE task until the next "await" statement
        run_once(loop)

    # Sleeping for half a second to wait for websocket connection termination
    loop.run_until_complete(asyncio.sleep(0.5))

    # Shutdown any async processes and close the event loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    print("Thank you for playing!")


if __name__ == "__main__":
    start_game()
