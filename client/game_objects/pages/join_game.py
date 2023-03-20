import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.scroll_text_tile import ScrollTextTile
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None
        self.scroll_text_tile = None
        self.build()

    def build(self):
        super().build()
        self.build_join_game_button()
        self.build_scrollable_text()

    def resize(self):
        super().resize()
        self.set_join_game_button_size()
        self.set_scroll_text_size()

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

    def build_scrollable_text(self):
        surface = pygame.image.load(f"{client.IMG_PATH}menu_field_croped.png").convert_alpha()
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_music_bar.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_button.png"
        ).convert_alpha()

        self.scroll_text_tile = ScrollTextTile(
            "hover",
            "slider",
            "handle",
            "left_arrow",
            "right_arrow",
            surface,
            slider_surface,
            slider_handle,
            self.event_handler.screen,
            50,
            130,
            200,
            [
                "some fucking shit",
                "test2",
                "test3",
                "test4",
                "test5",
                "test6",
                "test 7",
                "test 8",
                "test 9",
                "test 10",
                "test 11",
                "test 12",
            ],
            6,
            10
        )

        self.set_scroll_text_size()

    def set_scroll_text_size(self):
        if not self.scroll_text_tile:
            return

        self.scroll_text_tile.resize()
        self.scroll_text_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.scroll_text_tile.rect.centery = self.event_handler.screen_rect.centery

        self.scroll_text_tile.update()

        self.tiles_group.add(self.scroll_text_tile.right_arrow)
        self.tiles_group.add(self.scroll_text_tile.left_arrow)

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )

        self.event_handler.screen.blit(
            self.scroll_text_tile.image, self.scroll_text_tile.rect
        )
        self.scroll_text_tile.blit_text()

    def activate_tile(self, tile):
        if tile.name == "right_arrow":
            self.scroll_text_tile.next_text()
        if tile.name == "left_arrow":
            self.scroll_text_tile.previous_text()

        return None, False
