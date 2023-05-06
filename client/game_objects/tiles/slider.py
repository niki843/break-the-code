from typing import Any

import pygame

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
    tile_addition_width_percent : int
        used for addition to the width of the image that's being used, uses percent of the screen width
    tile_addition_height_percent : int
        used for addition to the height of the image that's being used, uses percent of the screen height
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
        handle_name,
        handle_surface,
        handle_size_percent,
        delimiters_count,
        handle_position,
        horizontal=True,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
        handle_height_percent=0,
        handle_width_percent=0
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )
        self.slider_handle = Tile(
            handle_name,
            handle_surface,
            screen,
            handle_size_percent,
            tile_addition_width_percent=handle_width_percent,
            tile_addition_height_percent=handle_height_percent
        )

        self.actual_percentage = []
        self.pivot_values = []
        self.delimiters = delimiters_count
        self.setup_percents()
        self.horizontal = horizontal

        self.handle_position = handle_position

        self.slider_percentage = (
            self.actual_percentage[self.handle_position] if self.delimiters >= 2 else 0
        )

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.delimiters = kwargs.get("delimiters") or self.delimiters
        self.setup_percents()
        self.update_slider_handle_by_position()

    def move_slider(self, event):
        self.move_slider_horizontally(
            event.pos[0]
        ) if self.horizontal else self.move_slider_vertically(event.pos[1])

    def move_slider_vertically(self, pos_y):
        if pos_y < self.rect.top or pos_y > self.rect.bottom:
            return

        self.handle_position = (
            bisect(
                self.pivot_values,
                round(((pos_y - self.rect.top) / self.image.get_height()) * 100),
            )
            - 1
        )

        self.update_slider_handle_by_position()

    def move_slider_horizontally(self, pos_x):
        if pos_x < self.rect.left or pos_x > self.rect.right:
            return

        self.handle_position = (
            bisect(
                self.pivot_values,
                round(((pos_x - self.rect.left) / self.image.get_width()) * 100),
            )
            - 1
        )

        self.update_slider_handle_by_position()

    def next_handle_position(self):
        self.set_value(1)

    def previous_handle_position(self):
        self.set_value(-1)

    def set_value(self, index):
        self.handle_position += index
        if self.handle_position < 0 or self.handle_position >= len(
            self.actual_percentage
        ):
            self.handle_position -= index
            return

        self.update_slider_handle_by_position()

    def update_slider_handle_by_position(self):
        if self.delimiters <= 1:
            return

        self.slider_percentage = self.actual_percentage[self.handle_position]
        slider_size = (
            self.image.get_width() if self.horizontal else self.image.get_height()
        )
        starting_position = self.rect.left if self.horizontal else self.rect.top

        if self.horizontal:
            self.slider_handle.rect.centerx = starting_position + (
                slider_size
                * common.get_percentage_multiplier_from_percentage(
                    self.slider_percentage
                )
            )
            return

        self.slider_handle.rect.centerx = self.rect.centerx
        if self.slider_percentage == 0:
            self.slider_handle.rect.top = starting_position + (
                slider_size
                * common.get_percentage_multiplier_from_percentage(
                    self.slider_percentage
                )
            )
        elif self.slider_percentage == 100:
            self.slider_handle.rect.bottom = starting_position + (
                slider_size
                * common.get_percentage_multiplier_from_percentage(
                    self.slider_percentage
                )
            )
        else:
            self.slider_handle.rect.centery = starting_position + (
                slider_size
                * common.get_percentage_multiplier_from_percentage(
                    self.slider_percentage
                )
            )

    def setup_percents(self):
        if self.delimiters <= 1:
            return
        self.actual_percentage = []
        self.pivot_values = []

        # -1 to compensate for the 0 value that will be first
        reference_value = 100 / (self.delimiters - 1)
        self.actual_percentage.append(0)
        self.pivot_values.append(-(reference_value / 2))
        # points of interests first element will be half of the reference value
        # this will allow the slider handle to move to the lower value if it's under
        # half of the slider's separation area and to the upper value if it's over
        for i in range(1, self.delimiters):
            self.actual_percentage.append(
                self.actual_percentage[i - 1] + reference_value
            )
            self.pivot_values.append(self.pivot_values[i - 1] + reference_value)
        # Because of float not being big enough and the final values sometimes is a little more than 100
        # we just set it as 100 this won't really be seen from the user
        self.actual_percentage[len(self.actual_percentage) - 1] = 100

    def set_slider_handle_position(self):
        if self.delimiters <= 1:
            self.slider_handle.rect.top = self.rect.top
            self.slider_handle.rect.left = self.rect.left
            return

        if self.horizontal:
            self.slider_handle.rect.centery = self.rect.centery
            self.slider_handle.rect.centerx = self.rect.left + (
                (self.image.get_width() / (self.delimiters - 1)) * self.handle_position
            )
        else:
            self.slider_handle.rect.centerx = self.rect.centerx
            if self.handle_position == len(self.actual_percentage) - 1:
                self.slider_handle.rect.bottom = self.rect.bottom
                return
            elif self.slider_percentage == 0:
                self.slider_handle.rect.top = self.rect.top + (
                    (self.image.get_height() / (self.delimiters - 1))
                    * self.handle_position
                )
            else:
                self.slider_handle.rect.centery = self.rect.top + (
                    (self.image.get_width() / (self.delimiters - 1))
                    * self.handle_position
                )

    def get_max_handle_position(self):
        return len(self.actual_percentage) - 1

    def resize(self):
        super().resize()
        if hasattr(self, "slider_handle"):
            self.slider_handle.resize()

    def get_index(self):
        """Returns the index of the percentage that the tile is currently on"""
        return self.handle_position

    def reset(self):
        self.handle_position = 0
        self.actual_percentage = []
        self.pivot_values = []
        self.setup_percents()
        self.slider_percentage = (
            self.actual_percentage[self.handle_position] if self.delimiters >= 2 else 0
        )

    def blit(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(
            self.slider_handle.image, self.slider_handle.rect
        )
