import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, screen):
        super().__init__(screen)

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()
