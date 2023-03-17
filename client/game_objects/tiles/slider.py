from client.game_objects.tiles.tile import Tile
from client.utils import common
from bisect import bisect


class Slider(Tile):
    """
    A class representing a slider image and a movable handle
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
    handle_name : str
        the name for the handle tile
    handle_surface : pygame.Surface
        the surface that will be used to build the Tile for the handle
    handle_size_percent : int
        a percent representation of the size of the handle, this is a percent from the slider image
    delimiters_count : int
        a number representing in how many equal parts the slider will be separated
    handle_position : int
        at which separation will the handle be placed
    """

    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        handle_name,
        handle_surface,
        handle_size_percent,
        delimiters_count,
        handle_position,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )
        self.slider_handle = Tile(
            handle_name, handle_surface, screen, handle_size_percent, 0, 0
        )

        self.actual_percentage = []
        self.points_of_interest = []
        self.setup_points_of_interest_and_percents(delimiters_count)

        self.handle_position = handle_position

        self.slider_percentage = 0
        self.delimiters = delimiters_count

    def move_slider(self, pos_x):
        if pos_x < self.rect.left or pos_x > self.rect.right:
            return

        self.handle_position = bisect(
            self.points_of_interest,
            round(
                int(((pos_x - self.rect.left) / self.image.get_width()) * 100)
                - (self.slider_handle.image.get_width() / 2),
                -1,
            ),
        )

        self.slider_percentage = self.actual_percentage[self.handle_position]
        self.slider_handle.rect.centerx = self.rect.left + (
            self.image.get_width()
            * common.get_percentage_multiplier_from_percentage(self.slider_percentage)
        )

    def setup_points_of_interest_and_percents(self, delimiters_count):
        # -1 to compensate for the 0 value that will be first
        reference_value = 100 / (delimiters_count - 1)
        self.actual_percentage.append(0)
        # points of interests first element will be half of the reference value
        # this will allow the slider handle to move to the lower value if it's under
        # half of the slider's separation area and to the upper value if it's over
        self.points_of_interest.append(reference_value / 2)
        for i in range(1, delimiters_count):
            self.actual_percentage.append(
                self.actual_percentage[i - 1] + reference_value
            )
            self.points_of_interest.append(
                self.actual_percentage[i - 1] + reference_value
            )

    def set_slider_handle_position(self):
        self.slider_handle.rect.centery = self.rect.centery
        self.slider_handle.rect.centerx = self.rect.left + (
            (self.image.get_width() / (self.delimiters - 1)) * self.handle_position
        )

    def resize(self):
        super().resize()
        if hasattr(self, "slider_handle"):
            self.slider_handle.resize()

    def get_index(self):
        """Returns the index of the percentage that the tile is currently on"""
        return self.handle_position
