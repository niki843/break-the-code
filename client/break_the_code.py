import pygame
import asyncio

import client
from client.server_communication_manager import ServerCommunicationManager
from client.state_manager import StateManager
from client.utils import common
from client.event_handler import EventHandler


def start_game():
    pygame.init()
    pygame.fastevent.init()
    pygame.mixer.init()

    pygame.mixer.music.load(f"{client.MUSIC_PATH}{client.DEFAULT_MUSIC}")
    pygame.mixer.music.set_volume(0.2)
    # Play the music on re-wind
    pygame.mixer.music.play(-1)

    # Disable the default cursor
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(client.DEFAULT_RESOLUTION_TUPLE, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption(client.GAME_NAME)

    thumbnail = common.get_image(client.DEFAULT_THUMBNAIL)
    pygame.display.set_icon(thumbnail)

    client.state_manager = StateManager(screen)

    client.server_communication_manager = ServerCommunicationManager()

    event_handler = EventHandler()

    while client.GAME_RUNNING:
        event_handler.current_window.blit()
        event_handler.current_window.position_and_blit_cursor()

        pygame.display.flip()
        events = pygame.event.get()

        for event in events:
            event_handler.handle_event(event)

        # tell event loop to run once
        # if there are no i/o events, this might return right away
        # if there are events or tasks that don't need to wait for i/o, then
        # run ONE task until the next "await" statement
        common.run_once(client.LOOP)

    # Sleeping for half a second to wait for websocket connection termination
    client.LOOP.run_until_complete(asyncio.sleep(client.ASYNC_SLEEP_TIME_ON_EXIT))

    # Shutdown any async processes and close the event loop
    client.LOOP.run_until_complete(client.LOOP.shutdown_asyncgens())
    client.LOOP.close()
    print("Thank you for playing!")


if __name__ == "__main__":
    start_game()
