from itertools import cycle

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

        character_width, character_height = self.font.size("a")

        self.max_characters_per_line = int(self.image.get_width() / character_width)
        print(f"max_characters_per_line: {self.max_characters_per_line}")
        self.max_lines_to_display = int(self.image.get_height() / (character_height + self.screen.get_height() * 0.015))
        print(f"max_lines_to_display {self.max_lines_to_display}")

    def load_font(self):
        self.text_size = int(
            self.image.get_height()
            * common.get_percentage_multiplier_from_percentage(self.text_size_percent)
        )
        self.font = common.load_font(self.text_size)

    def load_text(self):
        split_text = self.text.split(" ")
        lines = 1
        # This approach is making sure that we always start from 0 in the while
        # and in the beginning of each next loop we change the value to the next one
        # it's either this or a try finally, but I personally prefer this
        i = -1
        current_word = split_text[0]
        while i < len(split_text):
            i += 1

            # If the lines a too much for the text to fit in stop writing
            if lines > self.max_lines_to_display:
                break

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
                    current_word = current_word[:self.max_characters_per_line]
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

    def __add_text_to_text_surfaces(self, text):
        text_surface = self.font.render(
            text, True, client.GAME_BASE_COLOR
        )
        self.text_surfaces.append((text_surface, text_surface.get_rect()))

    def center_text(self):
        current_top_surface = self.rect.top
        for surface, rect in self.text_surfaces:
            rect.left = self.rect.left + (self.image.get_width() * 0.08)
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
