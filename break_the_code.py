import pygame
import os

from game_builder import GameBuilder


def start_game():
    pygame.init()

    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Break The Code")
    thumbnail = pygame.image.load(
        f".{os.path.sep}images{os.path.sep}crack-the-code-thumbnail.png"
    )
    pygame.display.set_icon(thumbnail)
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    GameBuilder()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    start_game()
