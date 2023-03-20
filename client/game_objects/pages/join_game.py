import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None
        self.build()

    def build(self):
        super().build()
        self.build_join_game_button()

    def resize(self):
        super().resize()
        self.set_join_game_button_size()

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_join_game_button(self):
        surface = pygame.image.load(f"{client.IMG_PATH}join_game.png").convert_alpha()

        self.join_game_tile = Tile(
            "join_game_button",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            10,
            0,
        )

        self.set_join_game_button_size()

    def set_join_game_button_size(self):
        if not self.join_game_tile:
            return

        self.join_game_tile.resize()
        self.join_game_tile.rect.right = self.event_handler.screen_rect.right - (
            self.event_handler.screen.get_width() * 0.04
        )
        self.join_game_tile.rect.bottom = self.event_handler.screen_rect.bottom - (
            self.event_handler.screen.get_height() * 0.05
        )
        self.tiles_group.add(self.join_game_tile)

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(self.join_game_tile.image, self.join_game_tile.rect)
