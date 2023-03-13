import pygame.image

import client
from client.game_objects.tiles.tile import Tile


class TextSlideshowTile(Tile):
    """
    A class used to create a Text Slideshow Tile, meaning a text that has a text shown on top
    and arrows to change the text using a list of strings

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
    initial_text : str
        the first string that will be displayed in the image box
    slide_values : list
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
        initial_text,
        slide_values: list,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.slide_values = slide_values
        self.current_text = initial_text

        self.current_text_surface = None
        self.current_text_rect = None

        self.right_arrow = None
        self.left_arrow = None

        self.font = None
        self.load_font()

        self.load_text()

        self.load_arrows()

    def update(self, *args, **kwargs) -> None:
        self.update_arrows_position()
        self.update_text_position()

    def update_arrows_position(self):
        self.right_arrow.rect.left = self.rect.right
        self.right_arrow.rect.centery = self.rect.centery

        self.left_arrow.rect.right = self.rect.left
        self.left_arrow.rect.centery = self.rect.centery

    def update_text_position(self):
        self.current_text_rect.centerx = self.rect.centerx
        self.current_text_rect.centery = self.rect.centery

    def load_font(self):
        self.font = pygame.font.Font(
            f"{client.FONT_PATH}SilkRemington-SBold.ttf",
            int(self.image.get_width() * 0.1),
        )

    def load_text(self):
        # Starting screen size will be the surfaces list mid element
        self.current_text_surface = self.font.render(
            self.current_text, True, client.GAME_BASE_COLOR
        )
        self.current_text_rect = self.current_text_surface.get_rect()

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

    def next_text(self):
        self.change_tile(1)

    def previous_text(self):
        self.change_tile(-1)

    def change_tile(self, tile_place: int):
        """Changes the current_text that's being displayed in the image box

        Parameters
        ----------
        tile_place : int
            An int that represents how many times and in which direction to get the wanted value from the list of texts
        """
        next_index = self.slide_values.index(self.current_text) + tile_place
        if next_index >= len(self.slide_values):
            next_index = 0

        self.current_text = self.slide_values[next_index]

        self.load_text()
        self.update_text_position()
