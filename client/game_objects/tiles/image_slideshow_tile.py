import pygame.image

import client
from client.game_objects.tiles.tile import Tile


# TODO: Not fully functional yet missing implentation for loading next/previous Tile and showing it as current
class ImageSlideshowTile(Tile):
    """
    A class used to create a Image Slideshow Tile, meaning that a list of images will be changed on arrow click
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
    slide_surfaces : list
        a list of the names of the pngs that will be displayed for next and previous
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
        slide_surfaces: list,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )

        self.surface = surface

        self.slides = slide_surfaces
        self.tiles = {}

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
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN
        )
        self.left_arrow = Tile(
            "screen_size_left_arrow",
            pygame.transform.flip(right_arrow_surface, True, True),
            self.screen,
            client.ARROW_WITH_PERCENTAGE_FROM_SCREEN
        )

    def build_next_tiles(
        self,
        name,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
    ):
        for slide in self.slides:
            self.surface = pygame.image.load(slide)
            self.tiles.update(
                {
                    self.surface: Tile(
                        name,
                        self.surface,
                        screen,
                        size_percent,
                        tile_addition_width,
                        tile_addition_height,
                    )
                }
            )

    def next(self):
        self.change_tile(1)

    def previous(self):
        self.change_tile(-1)

    def change_tile(self, addition_index):
        tiles_list = list(self.tiles)
        next_index = tiles_list.index(self.surface) + addition_index
        if next_index > len(tiles_list):
            next_index = 0
        next_surface = tiles_list[next_index]
        self.image = self.tiles.get(next_surface).image
        self.rect = self.tiles.get(next_surface).rect

    def resize(self):
        super().resize()
        if self.slides:
            for slide in self.slides:
                slide.resize()
