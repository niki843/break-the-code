import client

from client.game_objects.tiles.tile import Tile
from client.utils import common


class PlainTextTile(Tile):

    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        text_to_display: str,
        text_size_percent: int,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.text = text_to_display
        self.text_surface = None
        self.text_size_percent = text_size_percent
        self.font = None

        self.load_text()

    def load_text(self):
        text_size = int(
            self.image.get_height()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(text_size)
        self.text_surface = self.font.render(self.text, True, client.GAME_BASE_COLOR)

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self.load_text()
