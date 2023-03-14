import uuid

import pygame
import os
import asyncio
from client import ws_client as client, IMG_PATH, ASYNC_SLEEP_TIME_ON_EXIT, MUSIC_PATH
from client.game_objects.pages.menu import Menu
from client.event_handler import EventHandler

loop = asyncio.get_event_loop()

ws_client = client.WebsocketClient()


async def connect():
    print("Connecting to server")
    await ws_client.connect_to_server()
    print("Connected to server")


async def send_message(message):
    await ws_client.send_server_messages(message)

    print("Message sent")


def run_once():
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
            f.write("\nUnknown")

    # Open the player_id file and read the uuid
    with open("player_id.txt", "r") as f:
        player_details = f.read()

    return player_details.split("\n")


def start_game():
    # This will stay commented for testing and will be removed when
    # in actual release or specific testing of this feature
    player_id, username = get_or_generate_player_id()
    player_id = str(uuid.uuid4())

    pygame.init()
    pygame.fastevent.init()
    pygame.mixer.init()

    pygame.mixer.music.load(f"{MUSIC_PATH}main_music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()

    # Enable resizable mode currently not working !!!!!
    # screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Break The Code")

    thumbnail = pygame.image.load(f"{IMG_PATH}crack-the-code-thumbnail.png")
    pygame.display.set_icon(thumbnail)

    menu = Menu(screen)

    event_handler = EventHandler(player_id, current_window=menu, screen=screen)

    running = True
    while running:
        event_handler.current_window.blit()
        pygame.display.flip()
        events = pygame.event.get()

        for event in events:
            message, quit_game = event_handler.handle_event(event)

            if quit_game:
                running = False

            if message:
                loop.create_task(send_message(message))

        # tell event loop to run once
        # if there are no i/o events, this might return right away
        # if there are events or tasks that don't need to wait for i/o, then
        # run ONE task until the next "await" statement
        run_once()

    # Sleeping for half a second to wait for websocket connection termination
    loop.run_until_complete(asyncio.sleep(ASYNC_SLEEP_TIME_ON_EXIT))

    # Shutdown any async processes and close the event loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    print("Thank you for playing!")


if __name__ == "__main__":
    start_game()
