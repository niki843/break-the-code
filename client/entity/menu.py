from client import IMG_PATH
import pygame


class Menu:
    JOIN_GAME_POSITION = (0, 0)

    def __init__(self):
        self.new_game_tile = pygame.image.load(
            f"{IMG_PATH}new_game.png"
        )
        self.quit_tile = pygame.image.load(
            f"{IMG_PATH}quit.png"
        )
        self.settings_tile = pygame.image.load(
            f"{IMG_PATH}settings.png"
        )
        self.join_game_tile = pygame.image.load(
            f"{IMG_PATH}join_game.png"
        )

    def build(self):
        pass
