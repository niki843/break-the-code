from pygame import Color

import client
import pygame

from client.entity.join_game import JoinGame
from client.entity.new_game import NewGame
from client.entity.game_window import GameWindow
from client.entity.settings import Settings
from client.entity.tile import Tile


class Menu(GameWindow):
    def __init__(self, screen):
        super().__init__(screen)
        self.new_game_tile = None
        self.join_game_tile = None
        self.settings_tile = None
        self.quit_tile = None

        self.build()

    def build(self):
        # This order is important and should not change
        self.build_background()
        self.build_join_game()
        self.build_new_game()
        self.build_settings()
        self.build_quit_game()

    def build_join_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}join_game.png").convert_alpha()
        self.join_game_tile = Tile(
            "join_game",
            surface,
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )

        self.join_game_tile.rect.centerx = self.screen_rect.centerx
        self.join_game_tile.rect.centery = self.screen_rect.centery
        self.tiles_group.add(self.join_game_tile)

    def build_new_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}new_game.png").convert_alpha()
        self.new_game_tile = Tile(
            "new_game",
            surface,
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )

        self.new_game_tile.rect.centerx = self.screen_rect.centerx
        self.new_game_tile.rect.bottom = (
            self.join_game_tile.rect.top - client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.new_game_tile)

    def build_settings(self):
        surface = pygame.image.load(f"{client.IMG_PATH}settings.png").convert_alpha()
        self.settings_tile = Tile(
            "settings",
            surface,
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )

        self.settings_tile.rect.centerx = self.screen_rect.centerx
        self.settings_tile.rect.top = (
            self.join_game_tile.rect.bottom + client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.settings_tile)

    def build_quit_game(self):
        surface = pygame.image.load(f"{client.IMG_PATH}quit.png").convert_alpha()
        self.quit_tile = Tile(
            "quit_game",
            surface,
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )

        self.quit_tile.rect.right = (
            self.screen_rect.right - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.quit_tile.rect.top = (
            self.screen_rect.bottom
            - self.quit_tile.image.get_height()
            - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.tiles_group.add(self.quit_tile)

    def blit(self):
        # Refresh the object on the screen so any runtime changes will be reflected
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.join_game_tile.image, self.join_game_tile.rect)
        self.screen.blit(self.new_game_tile.image, self.new_game_tile.rect)
        self.screen.blit(self.settings_tile.image, self.settings_tile.rect)
        self.screen.blit(self.quit_tile.image, self.quit_tile.rect)

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

    def activate_tile(self, tile, event_handler):
        if tile.name == "new_game":
            event_handler.change_window(NewGame(self.screen))
        elif tile.name == "join_game":
            event_handler.change_window(JoinGame(self.screen))
        elif tile.name == "settings":
            event_handler.change_window(Settings(self.screen))
        elif tile.name == "quit_game":
            print("Closing the game")
            return '{"type": "close_connection"}', True

        self.delete()
        return None, False
