import pygame.image

import client
from client.entity.tile import Tile


# TODO: Not fully functional yet
class ImageSlideshowTile(Tile):
    """
    A class used to create a Image Slideshow Tile, meaning that a list of images will be changed on arrow click
    ...

    Attributes
    ----------
    name : str
        the name that will be used to reference the image tile
    surface : str
        the main surface on which the game is being displayed
    size_percent : str
        percent representation of what the size of the image compared to the surface would be
    tile_addition_width : int
        used for additional pixels to the width of the image that's being used
    tile_addition_height : int
        used for additional pixels to the height of the image that's being used
    slide_surfaces : list
        a list with the values that will be displayed in the image box
    """

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

        self.right_arrow = None
        self.left_arrow = None

        self.load_arrows()


    def update(self, *args, **kwargs) -> None:
        self.right_arrow.rect.left = self.rect.right
        self.right_arrow.rect.centery = self.rect.centery

        self.left_arrow.rect.right = self.rect.left
        self.left_arrow.rect.centery = self.rect.centery

    def load_arrows(self):
        right_arrow_surface = pygame.image.load(
            f"{client.IMG_PATH}next.png"
        ).convert_alpha()

        self.right_arrow = Tile(
            "screen_size_right_arrow",
            right_arrow_surface,
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
        self.left_arrow = Tile(
            "screen_size_left_arrow",
            pygame.transform.flip(right_arrow_surface, True, True),
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN,
            0,
            0,
        )
