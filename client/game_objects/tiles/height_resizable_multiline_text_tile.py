import math

from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.game_objects.tiles.tile import Tile
from client.utils import common


class HeightResizableMultilineTextTile(MultilineTextTile):
    def __init__(
        self,
        name,
        screen,
        width_percent,
        text_to_display: str,
        text_size_percent: float,
        start_line: int,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):

        self.text = text_to_display
        self.text_surfaces = []
        self.text_size_percent = text_size_percent
        self.start_line = start_line
        self.font = None
        self.text_size = 1

        self.load_font()
        self.new_line_space = self.screen.get_height() * 0.01

        self.character_width, self.character_height = self.font.size("h")

        self._load_max_characters_and_lines()

        height = (self.character_height + self.new_line_space) * self.lines_to_display

        surface = common.generate_transparent_image(self.screen.get_width() * common.get_percentage_multiplier_from_percentage(width_percent), height)

        super().__init__(
            name,
            surface,
            screen,
            width_percent,
            text_to_display,
            text_size_percent,
            start_line,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )

    def load_font(self):
        self.text_size = int(
            self.image.get_width()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(self.text_size)

    def _load_max_characters_and_lines(self):
        self.max_characters_per_line = int(
            self.image.get_width()
            / (self.character_width + self.character_width * 0.14)
        )
        self.lines_to_display = math.ceil(len(self.text) / self.max_characters_per_line)
