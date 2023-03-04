import uuid
import json

import pygame
import os
import asyncio
from client import ws_client as client, IMG_PATH
from client.entity.menu import Menu

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
    # This will stay commented for testing and will be removed when
    # in actual release or specific testing of this feature
    # player_id = get_or_generate_player_id()
    player_id = str(uuid.uuid4())

    pygame.init()
    pygame.fastevent.init()

    # Enable fullscreen mode
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Enable resizable mode currently not working !!!!!
    # screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Break The Code")

    thumbnail = pygame.image.load(
        f"{IMG_PATH}crack-the-code-thumbnail.png"
    )
    pygame.display.set_icon(thumbnail)

    menu = Menu(screen)

    running = True
    while running:
        menu.blit()
        pygame.display.flip()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                loop.create_task(send_message('{"type": "close_connection"}'))
                running = False
            if e.type == pygame.MOUSEBUTTONUP:
                if e.type == 1:
                    handle_mouse_click()
            elif e.type == client.EVENT_TYPE:
                print(e.message)
            elif e.type == pygame.KEYUP and e.key == pygame.K_n:
                loop.create_task(send_message(f'{{"type": "new_game", "player_id": "{player_id}", "player_name": "first_player"}}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_c:
                loop.create_task(send_message('{"type": "get_current_games"}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_j:
                game_session_id = input("game_session_id: ")
                loop.create_task(send_message(f'{{"type": "join_game", "player_id": "{player_id}", "player_name": "second_player", "game_session_id": "{game_session_id}"}}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_s:
                loop.create_task(send_message('{"type": "start_game"}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_p:
                condition_card_id = input("condition_card_id: ")
                loop.create_task(send_message(f'{{"type": "play_tile", "condition_card_id": {condition_card_id}}}'))
            elif e.type == pygame.KEYUP and e.key == pygame.K_o:
                condition_card_id = input("condition_card_id: ")
                card_number_choice = input("card_number_choice: ")
                loop.create_task(send_message(f'{{"type": "play_tile", "condition_card_id": {condition_card_id}, "card_number_choice": {card_number_choice}}}'))
            elif e.type == pygame and e.key == pygame.K_g:
                cards = []
                for i in range(0, 5):
                    cards.append(input(f"{i} card"))
                loop.create_task(send_message(f'{{"type": "guess_numbers", "player_guess": {json.dumps(cards)}}}'))



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


def handle_mouse_click():
    pass


if __name__ == "__main__":
    start_game()
