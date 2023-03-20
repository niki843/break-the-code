import client

from client.game_objects.tiles.tile import Tile
from client.utils import common


class HoverTextTile(Tile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        text_items: list,
        max_elements_to_display,
        text_size_percentage,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )
        self.text_list = text_items or []
        self.text_surfaces = []
        self.text_size = self.image.get_height() * common.get_percentage_multiplier_from_percentage(text_size_percentage)
        self.font = common.load_font(self.text_size)
        self.max_elements_to_display = max_elements_to_display
        self.first_element = 0

        self.create()

    def create(self):
        if self.text_surfaces:
            self.text_surfaces = []

        for idx, text in enumerate(self.text_list):
            if self.first_element > idx:
                continue

            if idx >= self.max_elements_to_display + self.first_element:
                break

            text_surface = self.font.render(text, True, client.GAME_BASE_COLOR)
            self.text_surfaces.append((text_surface, text_surface.get_rect()))

    def center(self):
        current_top_surface = self.rect.top
        for surface, rect in self.text_surfaces:
            rect.centerx = self.rect.centerx
            rect.top = current_top_surface + (self.screen.get_height() * 0.01)
            current_top_surface = rect.bottom

    def blit_text(self):
        for surface, rect in self.text_surfaces:
            self.screen.blit(surface, rect)

    def next_line(self):
        self.change_line(1)

    def previous_line(self):
        self.change_line(-1)

    def change_line(self, index):
        self.first_element += index

        if (
            self.max_elements_to_display + self.first_element > len(self.text_list)
            or self.first_element < 0
        ):
            self.first_element -= index
            return

        self.create()
        self.center()
