from client.game_objects.tiles.tile import Tile


class ToggleTile(Tile):

    def __init__(
            self,
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            slide_values: tuple,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.values = slide_values

    def next_value(self):
        index = self.values.index(self.image)

        if index > 1:
            index = 0

        self.image = self.values[index]
