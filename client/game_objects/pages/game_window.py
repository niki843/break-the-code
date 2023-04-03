import client
from pygame.sprite import LayeredUpdates

from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.game_objects.tiles.tile import Tile
from client.utils import common


class GameWindow:
    def __init__(self, event_handler):
        self.tiles_group = LayeredUpdates()

        self.event_handler = event_handler

        self.background_image = None
        self.back_tile = None
        self.tiles_background = None
        self.game_info_box = None

    def activate_tile(self, tile, event):
        pass

    def build(self):
        self.build_background()

    def resize(self):
        self.set_background_size()

    def build_background(self):
        surface = common.get_image("background.png")

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_clear_background(self):
        surface = common.get_image("clear_bgr.png")

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def set_background_size(self):
        self.background_image.resize()
        self.background_image.rect.centerx = self.event_handler.screen_rect.centerx
        self.background_image.rect.centery = self.event_handler.screen_rect.centery

    def build_back_tile(self):
        back_surface = common.get_image("back.png")
        self.back_tile = Tile(
            "back",
            back_surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            0,
            0,
        )

        self.set_back_tile()
        self.tiles_group.add(self.back_tile)

    def set_back_tile(self):
        if not self.back_tile:
            return

        self.back_tile.resize()
        self.back_tile.rect.left = self.event_handler.screen_rect.left + (
            self.event_handler.screen.get_width() * 0.03
        )
        self.back_tile.rect.top = self.event_handler.screen_rect.top + (
            self.event_handler.screen.get_height() * 0.03
        )

    def build_tiles_background(self):
        surface = common.get_image("menu_field_cropped.png")

        self.tiles_background = Tile(
            "tiles_background", surface, self.event_handler.screen, 80, 0, 0
        )
        self.set_tiles_background_size()

    def set_tiles_background_size(self):
        if not self.tiles_background:
            return
        self.tiles_background.resize()
        self.tiles_background.rect.centerx = self.event_handler.screen_rect.centerx
        self.tiles_background.rect.centery = self.event_handler.screen_rect.centery

    def build_game_info_box(self):
        surface = common.get_image("game_info_menu.png")
        self.game_info_box = MultilineTextTile(
            "game_info",
            surface,
            self.event_handler.screen,
            30,
            0,
            20,
            "",
            6,
            0,
        )

        self.set_game_info_size()

    def set_game_info_size(self):
        if not self.game_info_box:
            return

        self.game_info_box.resize()
        self.game_info_box.rect.centerx = self.event_handler.screen_rect.centerx
        self.game_info_box.rect.centery = self.event_handler.screen_rect.centery
        self.game_info_box.center_text()

    def blit(self):
        self.event_handler.screen.blit(
            self.background_image.image, self.background_image.rect
        )

    def open(self, **kwargs):
        self.event_handler.change_window(self)

    def close(self):
        pass
