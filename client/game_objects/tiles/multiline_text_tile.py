import client
from client.game_objects.tiles.tile import Tile
from client.utils import common


class MultilineTextTile(Tile):
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
        self.text_surfaces = []
        self.text_size_percent = text_size_percent
        self.font = None
        self.text_size = 1

        self.load_font()

        self.max_characters_per_line = int(self.image.get_width() / (self.text_size - self.text_size * 0.3))
        self.max_lines_to_display = int(self.image.get_height() / (self.text_size + self.screen.get_height() * 0.012))

    def load_font(self):
        self.text_size = int(
            self.image.get_height()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(self.text_size)

    def load_text(self):
        split_text = self.text.split(" ")
        current_word = split_text[0]
        lines = 1
        for i in range(1, len(split_text)):
            if lines > self.max_lines_to_display:
                break
            if len(current_word + split_text[i]) > self.max_characters_per_line:
                lines += 1
                text_surface = self.font.render(current_word, True, client.GAME_BASE_COLOR)
                self.text_surfaces.append((text_surface, text_surface.get_rect()))
                current_word = split_text[i]
                continue

            current_word += " " + split_text[i]

    def center_text(self):
        current_top_surface = self.rect.top
        for surface, rect in self.text_surfaces:
            rect.centerx = self.rect.centerx
            rect.top = current_top_surface + (self.screen.get_height() * 0.015)
            current_top_surface = rect.bottom

    def blit(self):
        for surface, rect in self.text_surfaces:
            self.screen.blit(surface, rect)

    def add_text(self, text_to_apply):
        self.text += text_to_apply
        self.load_text()

    def replace_text(self, new_text):
        self.text = new_text
        self.load_text()

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self.load_text()
