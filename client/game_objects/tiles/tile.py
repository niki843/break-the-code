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
    tile_addition_width : int
        used for additional pixels to the width of the image that's being used
    tile_addition_height : int
        used for additional pixels to the height of the image that's being used
    """

    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.image = surface

        self.screen = screen
        width, height = self.screen.get_size()
        self.standard_tile_width = width * common.get_percentage_multiplier_from_percentage(size_percent)

        self.standard_tile_height = (
            self.standard_tile_width * self.image.get_height() / self.image.get_width()
        )

        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.standard_tile_width) + tile_addition_width,
                int(self.standard_tile_height) + tile_addition_height,
            ),
        )

        self.rect = self.image.get_rect()

        self.screen.blit(self.image, self.rect)
