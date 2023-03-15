import pygame
from pygame.sprite import Group

from client import IMG_PATH


class GameWindow:
    def __init__(self, screen):
        self.tiles_group = Group()

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.background_image = None
        self.background_rect = None

    def activate_tile(self, tile, event_handler):
        return None, False

    def build(self):
        self.build_background()

    def build_background(self):
        self.background_image = pygame.image.load(
            f"{IMG_PATH}background.png"
        ).convert_alpha()

        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen.get_width(), self.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)

    def change_screen(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

    def delete(self):
        pass
