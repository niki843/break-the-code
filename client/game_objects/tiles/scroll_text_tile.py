import pygame

from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.game_objects.tiles.slider import Slider

from client.utils import common


class ScrollTextTile(MultilineTextTile):
    def __init__(
        self,
        name,
        slider_name,
        handle_name,
        main_background_surface,
        slider_surface,
        handle_surface,
        screen,
        size_percent,
        text_to_display: str,
        text_size_percentage: int,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        MultilineTextTile.__init__(
            self,
            name=name,
            surface=main_background_surface,
            screen=screen,
            size_percent=size_percent,
            text_to_display=text_to_display,
            text_size_percent=text_size_percentage,
            start_line=0,
            tile_addition_width_percent=tile_addition_width_percent,
            tile_addition_height_percent=tile_addition_height_percent,
        )

        self.load_text()

        delimiters = (
            (len(self.text_surfaces) - self.max_lines_to_display) + 1
            if self.text
            else 0
        )
        self.slider = Slider(
            name=slider_name,
            surface=slider_surface,
            screen=screen,
            size_percent=1,
            handle_name=handle_name,
            handle_surface=handle_surface,
            handle_size_percent=self.image.get_width() * 0.2,
            delimiters_count=delimiters,
            handle_position=0,
            horizontal=False,
        )

        self.resize_slider()

    def center_elements(self):
        self.slider.rect.right = self.rect.right - (self.image.get_width() * 0.02)
        self.slider.rect.centery = self.rect.centery

        self.slider.set_slider_handle_position()
        self.center_text()

    def move_slider(self, event):
        self.slider.move_slider(event)
        current_percentage = self.slider.slider_percentage

        if current_percentage > self.slider.slider_percentage:
            self.scroll_up()

        if current_percentage < self.slider.slider_percentage:
            self.scroll_down()

    def scroll_down(self):
        self.change_line(1)

    def scroll_up(self):
        self.change_line(-1)

    def change_line(self, index):
        self.start_line += index

        if (
            self.max_lines_to_display + self.start_line > len(self.text_surfaces)
            or self.start_line < 0
        ):
            self.start_line -= index
            return

        self.load_text()
        self.center_text()

    def resize(self):
        super().resize()

        if hasattr(self, "slider"):
            self.resize_slider()

    def resize_slider(self):
        width_slider = (
            self.image.get_width() * common.get_percentage_multiplier_from_percentage(5)
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

    def blit(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.slider.image, self.slider.rect)
        self.screen.blit(
            self.slider.slider_handle.image, self.slider.slider_handle.rect
        )
        super().blit()
