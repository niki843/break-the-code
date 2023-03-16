from client.game_objects.tiles.tile import Tile


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

    def set_slider_percentage(self):
        self.slider_percentage = int(
            (
                (self.slider_handle.rect.centerx - self.rect.left)
                / self.image.get_width()
            )
            * 100
        )

    def track_clicked_handle(self):
        pass

    def move_slider(self):
        pass
