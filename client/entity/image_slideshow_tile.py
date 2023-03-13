import pygame.image

import client
from client.entity.tile import Tile


class ImageSlideshowTile(Tile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        slide_surfaces: list,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.slides = slide_surfaces

        right_arrow_surface = pygame.image.load(
            f"{client.IMG_PATH}next.png"
        ).convert_alpha()

        self.right_arrow = Tile(
            "right_arrow_screen_size",
            right_arrow_surface,
            screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
        self.left_arrow = Tile(
            "left_arrow_screen_size",
            pygame.transform.flip(right_arrow_surface, True, True),
            screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )

    def update(self, *args, **kwargs) -> None:
        self.right_arrow.rect.left = self.rect.right
        self.right_arrow.rect.centery = self.rect.centery

        self.left_arrow.rect.right = self.rect.left
        self.left_arrow.rect.centery = self.rect.centery
