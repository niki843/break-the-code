import pygame
from pygame.sprite import Group

from client import IMG_PATH


class GameWindow:
    def __init__(self, event_handler):
        self.tiles_group = Group()

        self.event_handler = event_handler

        self.background_image = None
        self.background_rect = None

        self.build_background()

    def activate_tile(self, tile):
        return None, False

    def build(self):
        self.build_background()

    def build_background(self):
        self.background_image = pygame.image.load(
            f"{IMG_PATH}background.png"
        ).convert_alpha()

        self.background_image = pygame.transform.scale(
            self.background_image, (self.event_handler.screen.get_width(), self.event_handler.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

    def blit(self):
        self.event_handler.screen.blit(self.background_image, self.background_rect)

    def delete(self):
        pass
