from pygame.sprite import Group

from client import IMG_PATH, BETWEEN_TILE_AND_SCREEN_SPACING, BETWEEN_TILES_SPACING
import pygame

from client.entity.tile import Tile


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.tiles_group = Group()

        self.background_image = pygame.image.load(
            f"{IMG_PATH}background.png"
        ).convert_alpha()

        self.new_game_tile = None
        self.join_game_tile = None
        self.settings_tile = None
        self.quit_tile = None
        self.background_rect = None

        self.build()

    def build(self):
        # This order is important and should not change
        self.build_background()
        self.build_join_game()
        self.build_new_game()
        self.build_settings()
        self.build_quit_game()

    def build_background(self):
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen.get_width(), self.screen.get_height())
        )
        self.background_rect = self.background_image.get_rect()

    def build_join_game(self):
        surface = pygame.image.load(f"{IMG_PATH}new_game.png").convert_alpha()
        self.join_game_tile = Tile(surface, self.screen)

        self.join_game_tile.rect.centerx = self.screen_rect.centerx
        self.join_game_tile.rect.centery = self.screen_rect.centery
        self.tiles_group.add(self.join_game_tile)

    def build_new_game(self):
        surface = pygame.image.load(f"{IMG_PATH}new_game.png").convert_alpha()
        self.new_game_tile = Tile(surface, self.screen)

        self.new_game_tile.rect.centerx = self.screen_rect.centerx
        self.new_game_tile.rect.bottom = (
            self.join_game_tile.rect.top - BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.new_game_tile)

    def build_settings(self):
        surface = pygame.image.load(f"{IMG_PATH}settings.png").convert_alpha()
        self.settings_tile = Tile(surface, self.screen)

        self.settings_tile.rect.centerx = self.screen_rect.centerx
        self.settings_tile.rect.top = (
            self.join_game_tile.rect.bottom + BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.settings_tile)

    def build_quit_game(self):
        surface = pygame.image.load(f"{IMG_PATH}quit.png").convert_alpha()
        self.quit_tile = Tile(surface, self.screen)

        self.quit_tile.rect.right = (
            self.screen_rect.right - BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.quit_tile.rect.top = (
            self.screen_rect.bottom
            - self.quit_tile.image.get_height()
            - BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.tiles_group.add(self.quit_tile)

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.join_game_tile.image, self.join_game_tile.rect)
        self.screen.blit(self.new_game_tile.image, self.new_game_tile.rect)
        self.screen.blit(self.settings_tile.image, self.settings_tile.rect)
        self.screen.blit(self.quit_tile.image, self.quit_tile.rect)
