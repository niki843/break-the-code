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
        max_characters_on_line: int,
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
        self.text_rect = None
        self.text_size_percent = text_size_percent
        self.font = None
        self.max_characters_on_line = max_characters_on_line

        if len(self.text) > self.max_characters_on_line:
            self.text = self.text[:12]
            self.text += "..."

        self.load_text()

    def load_text(self):
        text_size = int(
            self.image.get_height()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(text_size)
        self.text_surface = self.font.render(self.text, True, client.GAME_BASE_COLOR)
        self.text_rect = self.text_surface.get_rect()

    def center(self):
        self.text_rect.centery = self.rect.centery
        self.text_rect.left = self.rect.left

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self.load_text()
