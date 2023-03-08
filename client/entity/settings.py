import pygame.image

from client import IMG_PATH
from client.entity.game_window import GameWindow
from client.entity.tile import Tile


class Settings(GameWindow):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen_size_tile = None

        self.build()

    def build(self):
        self.build_background()
        self.build_screen_size_tile()

    def build_screen_size_tile(self):
        screen_size_tile_surface = pygame.image.load(f"{IMG_PATH}settings_box.png")
        self.screen_size_tile = Tile("screen_size", screen_size_tile_surface, self.screen)

        self.screen_size_tile.rect.centerx = self.screen_rect.centerx
        self.screen_size_tile.rect.centery = self.screen_rect.centery

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.screen_size_tile.image, self.screen_size_tile.rect)
