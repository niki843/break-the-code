import pygame
from pygame.sprite import Group

from client import IMG_PATH
from client.game_objects.tiles.tile import Tile


class GameWindow:
    def __init__(self, event_handler):
        self.tiles_group = Group()

        self.event_handler = event_handler

        self.background_image = None

        self.build_background()

    def activate_tile(self, tile):
        return None, False

    def build(self):
        self.build_background()

    def resize(self):
        self.set_background_size()

    def build_background(self):
        surface = pygame.image.load(
            f"{IMG_PATH}background.png"
        ).convert_alpha()

        self.background_image = Tile("background", surface, self.event_handler.screen, 100, 0, 0)
        self.set_background_size()

    def set_background_size(self):
        self.background_image.resize()
        self.background_image.rect.centerx = self.event_handler.screen_rect.centerx
        self.background_image.rect.centery = self.event_handler.screen_rect.centery

    def blit(self):
        self.event_handler.screen.blit(self.background_image.image, self.background_image.rect)

    def delete(self):
        pass
