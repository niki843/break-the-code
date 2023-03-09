import pygame.image

from client import IMG_PATH
from client.entity.game_window import GameWindow
from client.entity.slideshow_tile import SlideshowTile
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
        surface = pygame.image.load(f"{IMG_PATH}1280x720.png").convert_alpha()
        self.screen_size_tile = SlideshowTile("screen_size", surface, self.screen)

        self.screen_size_tile.rect.centerx = self.screen_rect.centerx
        self.screen_size_tile.rect.centery = self.screen_rect.centery
        self.tiles_group.add(self.screen_size_tile)

        self.screen_size_tile.update()

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.screen_size_tile.image, self.screen_size_tile.rect)

    def activate_tile(self, tile, event_handler):
        if tile.name == "screen_size":
            return None, False
