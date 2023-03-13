import pygame.image
import client

from client.entity.game_window import GameWindow
from client.entity.tile import Tile


class Settings(GameWindow):
    SCREEN_SIZE_CAPTIONS = [
        "1024x620",
        "1280x720",
        "1366x768",
        "1536x864",
        "1720x880",
        "fullscreen",
    ]

    def __init__(self, screen):
        super().__init__(screen)
        self.screen_size_tile = None
        self.screen_size_right_arrow = None
        self.screen_size_left_arrow = None

        self.build()

    def build(self):
        self.build_background()
        self.build_screen_size_tile()

    def build_screen_size_tile(self):
        font = pygame.font.Font(f"{client.FONT_PATH}SilkRemington-SBold.ttf", 30)
        # Starting screen size will be the surfaces list mid element
        self.text = font.render(self.SCREEN_SIZE_CAPTIONS[int(len(self.SCREEN_SIZE_CAPTIONS) / 2)], True, (127, 169, 6))
        self.text_rect = self.text.get_rect()

        surface = pygame.image.load(f"{client.IMG_PATH}blank.png").convert_alpha()
        self.screen_size_tile = Tile(
            "screen_size", surface, self.screen, client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN, client.TILE_WIDTH_ADDITION, client.TILE_HEIGHT_ADDITION
        )

        right_arrow_surface = pygame.image.load(
            f"{client.IMG_PATH}next.png"
        ).convert_alpha()

        self.screen_size_right_arrow = Tile(
            "screen_size_right_arrow",
            right_arrow_surface,
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
        self.screen_size_left_arrow = Tile(
            "screen_size_left_arrow",
            pygame.transform.flip(right_arrow_surface, True, True),
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )

        self.screen_size_tile.rect.centerx = self.screen_rect.centerx
        self.screen_size_tile.rect.centery = self.screen_rect.centery

        self.text_rect.centerx = self.screen_size_tile.rect.centerx
        self.text_rect.centery = self.screen_size_tile.rect.centery

        self.screen_size_right_arrow.rect.left = self.screen_size_tile.rect.right
        self.screen_size_right_arrow.rect.centery = self.screen_size_tile.rect.centery

        self.screen_size_left_arrow.rect.right = self.screen_size_tile.rect.left
        self.screen_size_left_arrow.rect.centery = self.screen_size_tile.rect.centery

        self.tiles_group.add(self.screen_size_right_arrow)
        self.tiles_group.add(self.screen_size_left_arrow)

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.screen_size_tile.image, self.screen_size_tile.rect)
        self.screen.blit(
            self.screen_size_right_arrow.image,
            self.screen_size_right_arrow.rect,
        )
        self.screen.blit(
            self.screen_size_left_arrow.image,
            self.screen_size_left_arrow.rect,
        )
        self.screen.blit(self.text, self.text_rect)

    def activate_tile(self, tile, event_handler):
        if tile.name == "screen_size":
            return None, False
