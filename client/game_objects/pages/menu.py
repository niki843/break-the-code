from pygame import Color

import client
import pygame

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile


class Menu(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.new_game_tile = None
        self.join_game_tile = None
        self.settings_tile = None
        self.quit_tile = None

        self.build()

    def build(self):
        # This order is important and should not change
        super().build()
        self.build_join_game()
        self.build_new_game()
        self.build_settings()
        self.build_quit_game()

    def resize(self):
        super().resize()
        self.set_join_game_size()
        self.set_new_game_size()
        self.set_settings_size()
        self.set_quit_game_size()

    def build_join_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}join_game.png").convert_alpha()
        self.join_game_tile = Tile(
            "join_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_join_game_size()

    def set_join_game_size(self):
        if not self.join_game_tile:
            return

        self.join_game_tile.resize()
        self.join_game_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.join_game_tile.rect.centery = self.event_handler.screen_rect.centery
        self.tiles_group.add(self.join_game_tile)

    def build_new_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}new_game.png").convert_alpha()
        self.new_game_tile = Tile(
            "new_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_new_game_size()

    def set_new_game_size(self):
        if not self.new_game_tile:
            return

        self.new_game_tile.resize()
        self.new_game_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.new_game_tile.rect.bottom = (
            self.join_game_tile.rect.top - client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.new_game_tile)

    def build_settings(self):
        surface = pygame.image.load(f"{client.IMG_PATH}settings.png").convert_alpha()
        self.settings_tile = Tile(
            "settings",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_settings_size()

    def set_settings_size(self):
        if not self.settings_tile:
            return

        self.settings_tile.resize()
        self.settings_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.settings_tile.rect.top = (
            self.join_game_tile.rect.bottom + client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.settings_tile)

    def build_quit_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}quit.png").convert_alpha()
        self.quit_tile = Tile(
            "quit_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_quit_game_size()

    def set_quit_game_size(self):
        if not self.quit_tile:
            return

        self.quit_tile.resize()
        self.quit_tile.rect.right = (
            self.event_handler.screen_rect.right
            - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.quit_tile.rect.top = (
            self.event_handler.screen_rect.bottom
            - self.quit_tile.image.get_height()
            - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.tiles_group.add(self.quit_tile)

    def blit(self):
        # Refresh the object on the screen so any runtime changes will be reflected
        super().blit()
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )
        self.event_handler.screen.blit(
            self.new_game_tile.image, self.new_game_tile.rect
        )
        self.event_handler.screen.blit(
            self.settings_tile.image, self.settings_tile.rect
        )
        self.event_handler.screen.blit(self.quit_tile.image, self.quit_tile.rect)

    def delete(self):
        # Apparently pygame doesn't have an option to actually delete visual objects
        # instead we should just make them transparent
        self.background_image.fill(Color(0, 0, 0))
        self.join_game_tile.image.fill(Color(0, 0, 0))
        self.new_game_tile.image.fill(Color(0, 0, 0))
        self.settings_tile.image.fill(Color(0, 0, 0))
        self.quit_tile.image.fill(Color(0, 0, 0))

        self.blit()

        del self.background_image
        del self.join_game_tile
        del self.new_game_tile
        del self.settings_tile
        del self.quit_tile

        self.tiles_group.empty()

    def activate_tile(self, tile, event):
        if tile.name == "new_game" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.change_window(self.event_handler.new_game)
        elif tile.name == "join_game" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.change_window(self.event_handler.join_game)
        elif tile.name == "settings" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.change_window(self.event_handler.settings)
        elif tile.name == "quit_game" and event.button == client.LEFT_BUTTON_CLICK:
            print("Closing the game")
            return '{"type": "close_connection"}', True

        return None, False
