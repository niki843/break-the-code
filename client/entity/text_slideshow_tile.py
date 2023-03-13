import pygame.image

import client
from client.entity.tile import Tile


class TextSlideshowTile(Tile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        initial_text,
        slide_texts: list,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.slide_texts = slide_texts
        self.initial_text = initial_text

        self.current_text = None
        self.current_text_rect = None

        self.right_arrow = None
        self.left_arrow = None

        self.load_font()

        self.load_arrows()

    def update(self, *args, **kwargs) -> None:
        self.right_arrow.rect.left = self.rect.right
        self.right_arrow.rect.centery = self.rect.centery

        self.left_arrow.rect.right = self.rect.left
        self.left_arrow.rect.centery = self.rect.centery

        self.current_text_rect.centerx = self.rect.centerx
        self.current_text_rect.centery = self.rect.centery

    def load_font(self):
        font = pygame.font.Font(f"{client.FONT_PATH}SilkRemington-SBold.ttf", int(self.image.get_width() * 0.1))
        # Starting screen size will be the surfaces list mid element
        self.current_text = font.render(self.initial_text, True, client.GAME_BASE_COLOR)
        self.current_text_rect = self.current_text.get_rect()

    def load_arrows(self):
        right_arrow_surface = pygame.image.load(
            f"{client.IMG_PATH}next.png"
        ).convert_alpha()

        self.right_arrow = Tile(
            "right_arrow_screen_size",
            right_arrow_surface,
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
        self.left_arrow = Tile(
            "left_arrow_screen_size",
            pygame.transform.flip(right_arrow_surface, True, True),
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
