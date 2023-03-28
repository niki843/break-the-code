import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

    def build(self):
        super().build()

    def resize(self):
        super().resize()

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def blit(self):
        super().blit()

    def delete(self):
        super().delete()
