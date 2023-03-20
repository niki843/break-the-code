import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.hover_text_tile import HoverTextTile
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None
        self.hoverable_text_tile = None
        self.build()

    def build(self):
        super().build()
        self.build_join_game_button()
        self.build_hoverable_text()

    def resize(self):
        super().resize()
        self.set_join_game_button_size()
        self.set_hoverable_text_size()

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

    def build_hoverable_text(self):
        surface = pygame.image.load(f"{client.IMG_PATH}blank.png").convert_alpha()

        self.hoverable_text_tile = HoverTextTile(
            "hover",
            surface,
            self.event_handler.screen,
            30,
            0,
            0,
            [
                "some fucking shit",
                "test2",
                "test3",
                "test4",
                "test5",
                "test6",
                "test 7",
            ],
            6,
            15
        )

        self.set_hoverable_text_size()

    def set_hoverable_text_size(self):
        if not self.hoverable_text_tile:
            return

        self.hoverable_text_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.hoverable_text_tile.rect.centery = self.event_handler.screen_rect.centery

        self.hoverable_text_tile.center()

        self.tiles_group.add(self.hoverable_text_tile)

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )

        self.event_handler.screen.blit(
            self.hoverable_text_tile.image, self.hoverable_text_tile.rect
        )
        self.hoverable_text_tile.blit_text()

    def activate_tile(self, tile):
        if tile.name == "hover":
            self.hoverable_text_tile.next_line()

        return None, False
