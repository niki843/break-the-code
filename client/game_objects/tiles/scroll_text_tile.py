import pygame

import client
from client.game_objects.tiles.slider import Slider
from client.game_objects.tiles.text_slideshow_tile import TextSlideshowTile

from client.utils import common


class ScrollTextTile(TextSlideshowTile):
    def __init__(
        self,
        name,
        slider_name,
        handle_name,
        left_arrow_name,
        right_arrow_name,
        main_background_surface,
        slider_surface,
        handle_surface,
        screen,
        size_percent,
        arrow_size_percent,
        slider_size_percent,
        slider_handle_size_percent,
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
        self.scroll_delimiters = (
            len(text_items) - max_elements_to_display + 1 if text_items else 0
        )
        self.old_rect = None

        super().__init__(
            name,
            left_arrow_name,
            right_arrow_name,
            main_background_surface,
            screen,
            size_percent,
            arrow_size_percent,
            tile_addition_width,
            tile_addition_height,
            None,
            text_items or [],
            horizontal=False,
        )
        self.slider = Slider(
            name=slider_name,
            surface=slider_surface,
            screen=screen,
            size_percent=1,
            tile_addition_width=0,
            tile_addition_height=0,
            handle_name=handle_name,
            handle_surface=handle_surface,
            handle_size_percent=self.image.get_width() * 0.2,
            delimiters_count=self.scroll_delimiters,
            handle_position=0,
            horizontal=False,
        )
        self.slider_size_percent = slider_size_percent
        self.slider_handle_size_percent = slider_handle_size_percent

        self.resize_slider()

        self.text_size = int(
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
        self.slider.rect.right = self.rect.right - (self.image.get_width() * 0.02)
        self.slider.rect.centery = self.rect.centery

        self.slider.set_slider_handle_position()

        self.right_arrow.rect.centerx = self.slider.rect.centerx
        self.right_arrow.rect.bottom = self.rect.bottom

        self.left_arrow.rect.centerx = self.slider.rect.centerx
        self.left_arrow.rect.top = self.rect.top

    def update_text_position(self):
        current_top_surface = self.rect.top + 50
        for surface, rect in self.text_surfaces:
            rect.centerx = self.rect.centerx
            rect.top = current_top_surface + (self.screen.get_height() * 0.015)
            current_top_surface = rect.bottom

    def move_slider(self, event):
        current_percentage = self.slider.slider_percentage
        self.slider.move_slider_horizontally(
            event.pos[0]
        ) if self.horizontal else self.slider.move_slider_vertically(event.pos[1])

        if current_percentage > self.slider.slider_percentage:
            self.previous_text()

        if current_percentage < self.slider.slider_percentage:
            self.next_text()

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
        self.update_text_position()

    def resize(self):
        super().resize()
        if hasattr(self, "font"):
            self.text_size = int(
                self.image.get_width()
                * common.get_percentage_multiplier_from_percentage(
                    self.text_size_percentage
                )
            )
            self.font = common.load_font(self.text_size)
            self.load_text()

        if hasattr(self, "slider"):
            self.slider.screen = self.screen
            self.resize_slider()

    def resize_slider(self):
        width_slider = (
            self.image.get_width()
            * common.get_percentage_multiplier_from_percentage(5)
        )
        self.slider.image = pygame.transform.scale(
            self.slider.image,
            (
                width_slider,
                self.image.get_height() - (self.image.get_height() * 0.1),
            ),
        )
        self.slider.rect = self.slider.image.get_rect()

        self.slider.slider_handle.image = pygame.transform.scale(
            self.slider.slider_handle.image,
            (
                width_slider,
                width_slider
                * self.slider.slider_handle.original_image.get_height()
                / self.slider.slider_handle.original_image.get_width(),
            ),
        )
        self.slider.slider_handle.rect = self.slider.slider_handle.image.get_rect()

    def blit_text(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.right_arrow.image, self.right_arrow.rect)
        self.screen.blit(self.left_arrow.image, self.left_arrow.rect)
        self.screen.blit(self.slider.image, self.slider.rect)
        self.screen.blit(
            self.slider.slider_handle.image, self.slider.slider_handle.rect
        )
        self.old_rect = self.slider.slider_handle.rect
        for surface, rect in self.text_surfaces:
            self.screen.blit(surface, rect)
