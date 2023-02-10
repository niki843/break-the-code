import pygame
import os
import asyncio
import threading

from client import ws_client as client

img_path = f".{os.path.sep}images{os.path.sep}"


ws_client = client.WebsocketClient()


def start_server(loop, future):
    loop.run_until_complete(ws_client.connect_to_server())


def send_message(message, future):
    print(message)
    asyncio.run(ws_client.send_server_messages('{"type": "new_game", "player_id": "0ed61f48-2761-4c82-9460-788af1f52795", "player_name": "first_player"}'))


def stop_server(loop, future):
    loop.call_soon_threadsafe(future.set_result, None)


def start_game():
    # Create a server client and connect to the server
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    thread = threading.Thread(target=start_server, args=(loop, future))
    thread.start()

    pygame.init()
    # screen dimensions
    HEIGHT = 320
    WIDTH = 480

    # set up the drawing window
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    color = pygame.Color('blue')
    radius = 30
    x = int(WIDTH / 2)

    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Break The Code")
    thumbnail = pygame.image.load(
        f"{img_path}crack-the-code-thumbnail.png"
    )
    pygame.display.set_icon(thumbnail)

    background = pygame.image.load(f"{img_path}background.png")
    screen.blit(pygame.transform.scale(background, (1280, 720)), (0, 0))
    pygame.display.flip()

    running = True
    while running:
        # did the user close the window
        for event in pygame.fastevent.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == client.EVENT_TYPE:
                print(event.message)
                color = pygame.Color('red')
                x = (x + radius / 3) % (WIDTH - radius * 2) + radius
            elif event.type == pygame.KEYDOWN:
                color = pygame.Color('red')
                x = (x + radius / 3) % (WIDTH - radius * 2) + radius
                thread = threading.Thread(target=send_message, args=("test", future))
                thread.start()

    end_game(loop, future, thread)


def end_game(loop, future, thread):
    print("Stoping event loop")
    stop_server(loop, future)
    print("Waiting for termination")
    thread.join()
    print("Shutdown pygame")
    pygame.quit()


if __name__ == "__main__":
    start_game()
