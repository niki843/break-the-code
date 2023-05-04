import math
import client

from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
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
    ):
        self.text = text_to_display
        self.width_percent = width_percent
        self.new_line_space = screen.get_height() * 0.01
        font = common.load_font(
            (client.state_manager.screen.get_width() * common.get_percentage_multiplier_from_percentage(width_percent))
            * common.get_percentage_multiplier_from_percentage(text_size_percent)
        )
        self.character_width, self.character_height = font.size("h")

        self._load_max_characters_and_lines()

        surface = common.generate_transparent_image(screen.get_width() * common.get_percentage_multiplier_from_percentage(width_percent), self.height)

        super().__init__(
            name,
            surface,
            screen,
            width_percent,
            text_to_display,
            text_size_percent,
            start_line,
            0,
            0,
        )

    def _load_max_characters_and_lines(self):
        self.max_characters_per_line = int(
            (client.state_manager.screen.get_width() * common.get_percentage_multiplier_from_percentage(self.width_percent))
            / (self.character_width + self.character_width * 0.14)
        )
        self.max_lines_to_display = math.ceil(len(self.text) / self.max_characters_per_line)
        self.height = (self.character_height + self.new_line_space) * self.max_lines_to_display

    def resize(self):
        self._load_max_characters_and_lines()
        self.surface = common.generate_transparent_image(self.screen.get_width() * common.get_percentage_multiplier_from_percentage(self.width_percent), self.height)
        super().resize()
