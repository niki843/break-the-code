import pygame

import client
from pygame.sprite import LayeredUpdates

from client.game_objects.groups.player_info_group import PlayerInfoGroup
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
        self.player_info_group = None

        self.cursor = Tile(
            "cursor",
            common.get_image("cursor.png"),
            client.state_manager.screen,
            2,
        )

    def activate_tile(self, tile, event):
        match event.button:
            case client.LEFT_BUTTON_CLICK:
                self.tile_left_button_click_event(tile)
            case client.SCROLL_UP:
                self.tile_scroll_up_event(tile)
            case client.SCROLL_DOWN:
                self.tile_scroll_down_event(tile)

    def tile_left_button_click_event(self, tile):
        pass

    def tile_scroll_up_event(self, tile):
        pass

    def tile_scroll_down_event(self, tile):
        pass

    def build(self):
        self.build_background()

    def resize(self):
        self.set_background_size()

    def build_background(self):
        surface = common.get_image("background.png")
        self.load_background_and_resize(surface)

    def build_clear_background(self):
        surface = common.get_image("clear_bgr.png")
        self.load_background_and_resize(surface)

    def build_new_game_background(self):
        surface = common.get_image("new_game_bgr.png")
        self.load_background_and_resize(surface)

    def load_background_and_resize(self, surface):
        self.background_image = Tile(
            "background", surface, client.state_manager.screen, 100
        )
        self.set_background_size()

    def set_background_size(self):
        self.background_image.resize()
        self.background_image.rect.centerx = client.state_manager.screen_rect.centerx
        self.background_image.rect.centery = client.state_manager.screen_rect.centery

    def build_back_tile(self):
        back_surface = common.get_image("back.png")
        self.back_tile = Tile(
            "back",
            back_surface,
            client.state_manager.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL
        )

        self.set_back_tile()
        self.tiles_group.add(self.back_tile)

    def set_back_tile(self):
        if not self.back_tile:
            return

        self.back_tile.resize()
        self.back_tile.rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.03
        )
        self.back_tile.rect.top = client.state_manager.screen_rect.top + (
            client.state_manager.screen.get_height() * 0.03
        )

    def build_tiles_background(self):
        surface = common.get_image("menu_field_cropped.png")

        self.tiles_background = Tile(
            "tiles_background", surface, client.state_manager.screen, 84
        )
        self.set_tiles_background_size()

    def set_tiles_background_size(self):
        if not self.tiles_background:
            return
        self.tiles_background.resize()
        self.tiles_background.rect.centerx = client.state_manager.screen_rect.centerx
        self.tiles_background.rect.centery = client.state_manager.screen_rect.centery

    def build_game_info_box(self):
        surface = common.get_image("game_info_menu.png")
        self.game_info_box = Tile(
            name="game_info",
            surface=surface,
            screen=client.state_manager.screen,
            size_percent=30,
            tile_addition_height_percent=1.6,
        )

        self.set_game_info_size()

    def set_game_info_size(self):
        if not self.game_info_box:
            return

        self.game_info_box.resize()
        self.game_info_box.rect.centerx = client.state_manager.screen_rect.centerx
        self.game_info_box.rect.centery = client.state_manager.screen_rect.centery

    def build_player_info_group(self):
        left, top = self.get_player_info_initial_position()
        self.player_info_group = PlayerInfoGroup(
            "player_info_group",
            0,
            left,
            top,
            client.state_manager.screen,
        )

        self.set_player_info_group_size()

    def set_player_info_group_size(self):
        if not self.player_info_group:
            return

        left, top = self.get_player_info_initial_position()

        self.player_info_group.first_element_left_position = left
        self.player_info_group.first_element_top_position = top
        self.player_info_group.resize()

    def get_player_info_initial_position(self):
        left = self.game_info_box.rect.left + (
            client.state_manager.screen.get_width() * 0.02
        )
        top = self.game_info_box.rect.top + (
            client.state_manager.screen.get_height() * 0.02
        )
        return left, top

    def blit(self):
        client.state_manager.screen.blit(
            self.background_image.image, self.background_image.rect
        )

    def position_and_blit_cursor(self):
        self.cursor.rect.left, self.cursor.rect.top = pygame.mouse.get_pos()
        self.cursor.rect.left = self.cursor.rect.left - (
            self.cursor.image.get_width() * 0.14
        )
        client.state_manager.screen.blit(self.cursor.image, self.cursor.rect)

    def open(self, **kwargs):
        self.event_handler.change_window(self)

    def start_game(self, **kwargs):
        pass

    def close(self):
        pass

