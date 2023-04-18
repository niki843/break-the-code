import pygame.sprite
from pygame import sprite

from client.utils import common


class Tile(sprite.Sprite):
    """
    A class representing a tile image
    ...

    Attributes
    ----------
    name : str
        the name that will be used to reference the image tile
    surface : pygame.Surface
        the surface that will be displayed as a tile and used to show text on top
    screen : pygame.Surface
        the main surface on which the game is being displayed
    size_percent : str
        percent representation of what the size of the image compared to the surface would be
    tile_addition_width_percent : int
        used for addition to the width of the image that's being used, uses percent of the screen width
    tile_addition_height_percent : int
        used for addition to the height of the image that's being used, uses percent of the screen height
    """

    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.original_image = surface
        self.image = surface
        self.rect = None
        self.priority = 0

        self.screen = screen
        self.size_percent = size_percent
        self.tile_addition_width_percent = tile_addition_width_percent
        self.tile_addition_height_percent = tile_addition_height_percent

        self.standard_tile_width = None
        self.standard_tile_height = None

        self.resize()

    def resize(self):
        width, height = self.screen.get_size()
        self.standard_tile_width = (
            width * common.get_percentage_multiplier_from_percentage(self.size_percent)
        )

        self.standard_tile_height = (
            self.standard_tile_width
            * self.original_image.get_height()
            / self.original_image.get_width()
        )

        self.image = pygame.transform.scale(
            self.original_image,
            (
                int(self.standard_tile_width) + (self.screen.get_width() * common.get_percentage_multiplier_from_percentage(self.tile_addition_width_percent)),
                int(self.standard_tile_height) + (self.screen.get_height() * common.get_percentage_multiplier_from_percentage(self.tile_addition_height_percent)),
            ),
        )

        self.rect = self.image.get_rect()
