import pygame
import os
from utils.game_events import check_events

img_path = f".{os.path.sep}images{os.path.sep}"


def start_game():
    pygame.init()

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
        running = check_events(background, screen) is None
        pygame.display.update()


if __name__ == "__main__":
    start_game()
