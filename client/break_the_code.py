import uuid

import pygame
import asyncio

from client.server_communication_manager import ServerCommunicationManager
from client.utils import common
from client import (
    IMG_PATH,
    ASYNC_SLEEP_TIME_ON_EXIT,
    MUSIC_PATH,
    LOOP,
)
from client.event_handler import EventHandler


def start_game():
    player_id, username = common.get_or_generate_player_id()
    # TODO: Remove this when testing is done
    player_id = str(uuid.uuid4())

    pygame.init()
    pygame.fastevent.init()
    pygame.mixer.init()

    pygame.mixer.music.load(f"{MUSIC_PATH}main_music.mp3")
    pygame.mixer.music.set_volume(0.2)
    # Play the music on re-wind
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Break The Code")

    thumbnail = pygame.image.load(f"{IMG_PATH}logo_thumbnail.png")
    pygame.display.set_icon(thumbnail)

    server_communication_manager = ServerCommunicationManager(player_username=username, player_id=player_id)

    event_handler = EventHandler(player_id=player_id, username=username, screen=screen, server_communication_manager=server_communication_manager)

    running = True
    while running:
        event_handler.current_window.blit()
        pygame.display.flip()
        events = pygame.event.get()

        for event in events:
            quit_game = event_handler.handle_event(event)

            running = not quit_game

        # tell event loop to run once
        # if there are no i/o events, this might return right away
        # if there are events or tasks that don't need to wait for i/o, then
        # run ONE task until the next "await" statement
        common.run_once(LOOP)

    # Sleeping for half a second to wait for websocket connection termination
    LOOP.run_until_complete(asyncio.sleep(ASYNC_SLEEP_TIME_ON_EXIT))

    # Shutdown any async processes and close the event loop
    LOOP.run_until_complete(LOOP.shutdown_asyncgens())
    LOOP.close()
    print("Thank you for playing!")


if __name__ == "__main__":
    start_game()
