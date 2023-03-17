from client.game_objects.tiles.tile import Tile
from client.utils import common


class Slider(Tile):
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

        self.slider_percentage = 0
        self.delimiters = delimiters_count

    def move_slider(self, pos_x):
        if pos_x < self.rect.left or pos_x > self.rect.right:
            return

        self.slider_percentage = round(int(
            (
                (pos_x - self.rect.left)
                / self.image.get_width()
            )
            * 100
        ), -1)
        self.slider_handle.rect.centerx = self.rect.left + (self.image.get_width() * common.get_percentage_multiplier_from_percentage(self.slider_percentage))

        print(self.slider_percentage)

    def resize(self):
        super().resize()
        if hasattr(self, "slider_handle"):
            self.slider_handle.resize()
