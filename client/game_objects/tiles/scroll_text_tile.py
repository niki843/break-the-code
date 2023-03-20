import client
from client.game_objects.tiles.text_slideshow_tile import TextSlideshowTile

from client.utils import common


class ScrollTextTile(TextSlideshowTile):
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
        self.text_surfaces = []
        self.first_element = 0
        self.max_elements_to_display = max_elements_to_display
        self.text_size_percentage = text_size_percentage

        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            None,
            text_items or [],
            horizontal=False
        )

        self.text_size = (
            self.image.get_height()
            * common.get_percentage_multiplier_from_percentage(text_size_percentage)
        )
        self.font = common.load_font(self.text_size)

    def load_text(self):
        if self.text_surfaces:
            self.text_surfaces = []

        for idx, text in enumerate(self.slide_values):
            if self.first_element > idx:
                continue

            if idx >= self.max_elements_to_display + self.first_element:
                break

            text_surface = self.font.render(text, True, client.GAME_BASE_COLOR)
            self.text_surfaces.append((text_surface, text_surface.get_rect()))

    def update_arrows_position(self):
        self.right_arrow.rect.right = self.rect.right
        self.right_arrow.rect.top = self.rect.top

        self.left_arrow.rect.right = self.rect.right
        self.left_arrow.rect.bottom = self.rect.bottom

    def update_text_position(self):
        current_top_surface = self.rect.top + 50
        for surface, rect in self.text_surfaces:
            rect.centerx = self.rect.centerx
            rect.top = current_top_surface + (self.screen.get_height() * 0.015)
            current_top_surface = rect.bottom

    def next_text(self):
        self.change_tile(1)

    def previous_text(self):
        self.change_tile(-1)

    def change_tile(self, index):
        self.first_element += index

        if (
            self.max_elements_to_display + self.first_element > len(self.slide_values)
            or self.first_element < 0
        ):
            self.first_element -= index
            return

        self.load_text()
        self.update()

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self.text_size = (
                self.image.get_height()
                * common.get_percentage_multiplier_from_percentage(
                    self.text_size_percentage
                )
            )
            self.font = common.load_font(self.text_size)
            self.load_text()

    def blit_text(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.right_arrow.image, self.right_arrow.rect)
        self.screen.blit(self.left_arrow.image, self.left_arrow.rect)
        for surface, rect in self.text_surfaces:
            self.screen.blit(surface, rect)
