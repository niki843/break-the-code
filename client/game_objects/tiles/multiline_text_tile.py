import client
from client.game_objects.tiles.tile import Tile
from client.utils import common
from client.utils.enums import AlignType


class MultilineTextTile(Tile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        text_to_display: str,
        text_size_percent: float,
        start_line: int,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        super().__init__(
            name=name,
            surface=surface,
            screen=screen,
            size_percent=size_percent,
            tile_addition_width_percent=tile_addition_width_percent,
            tile_addition_height_percent=tile_addition_height_percent,
        )

        self.text = text_to_display
        self.text_surfaces = []
        self.text_size_percent = text_size_percent
        self.font = None
        self.text_size = 1
        self.start_line = start_line

        self.load_font()
        self.new_line_space = self.screen.get_height() * 0.01
        self.text_left_spacing = self.image.get_width() * 0.07

        self.character_width, self.character_height = self.font.size("h")

        self._load_max_characters_and_lines()

    def load_font(self):
        self.text_size = int(
            self.image.get_width()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(self.text_size)

    def load_text(self):
        self.text_surfaces = []
        split_text = self.text.split(" ")
        lines = 1
        # This approach is making sure that we always start from 0 in the while
        # and in the beginning of each next loop we change the value to the next one
        # it's either this or a try finally, but I personally prefer this
        i = -1
        current_word = split_text[0]
        while i < len(split_text):
            i += 1

            next_word = ""
            if i < len(split_text) - 1:
                next_word = split_text[i + 1]

            if (
                i == len(split_text) - 1
                or len(current_word + next_word) >= self.max_characters_per_line
                or next_word == "\n"
            ):
                # Check if the current_word isn't too big
                if len(current_word) > self.max_characters_per_line:
                    # if it is too big we split it by the maximum chars per line
                    # and set current_word = the second part of the split word
                    next_word = current_word[self.max_characters_per_line:]
                    current_word = current_word[: self.max_characters_per_line]
                    # finally, we subtract the index by one making sure that in the next iteration we will be
                    # considering i to be the same word_index as before
                    i -= 1
                lines += 1
                text_surface = self.font.render(
                    current_word, True, client.GAME_BASE_COLOR
                )
                self.text_surfaces.append((text_surface, text_surface.get_rect()))
                current_word = next_word.replace("\n", "")
                continue

            current_word += " " + next_word
            current_word = current_word.lstrip(" ")

    def center_text(self, align_type=AlignType.LEFT):
        current_top_surface = self.rect.top
        displayed_surfaces = self.text_surfaces[
            self.start_line : self.start_line + self.max_lines_to_display
        ]
        for surface, rect in displayed_surfaces:
            if align_type == AlignType.LEFT:
                rect.left = self.rect.left + self.text_left_spacing
            elif align_type == AlignType.CENTER:
                rect.centerx = self.rect.centerx
            else:
                rect.right = self.rect.right + self.text_left_spacing
            rect.top = current_top_surface
            current_top_surface = rect.bottom + self.new_line_space

    def blit(self):
        self.screen.blit(self.image, self.rect)

        displayed_surfaces = self.text_surfaces[
            self.start_line: self.start_line + self.max_lines_to_display
        ]
        for surface, rect in displayed_surfaces:
            self.screen.blit(surface, rect)

    def add_text(self, text_to_apply):
        self.text += text_to_apply
        self.load_text()

    def replace_text(self, new_text):
        self.text = new_text
        self.load_text()

    def _load_max_characters_and_lines(self):
        self.max_characters_per_line = int(
            self.image.get_width()
            / (self.character_width + self.character_width * 0.14)
        )
        self.max_lines_to_display = int(
            self.image.get_height() / (self.character_height + self.new_line_space)
        )

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self._load_max_characters_and_lines()
            self.load_font()
            self.load_text()
