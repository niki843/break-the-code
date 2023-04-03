import pygame

from client.game_objects.tiles.plain_text_box import PlainTextTile


class Dropdown:
    def __init__(
        self,
        first_tile_name,
        first_tile_text,
        surface,
        dropdown_name_text_map,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
    ):
        self.first_tile = self.create_dropdown_tile(
            first_tile_name,
            screen,
            surface,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            first_tile_text,
        )

        self.dropdown_surfaces = []
        self.active = False
        self.screen = screen

        for name, text in dropdown_name_text_map.items():
            self.create_dropdown_tile(
                name,
                screen,
                surface,
                size_percent,
                tile_addition_width,
                tile_addition_height,
                text
            )

    def create_dropdown_tile(self, name, screen, surface, size_percent, tile_addition_width, tile_addition_height, first_tile_text):
        return PlainTextTile(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            text_to_display=first_tile_text,
            text_size_percent=70,
            max_characters_on_line=1,
        )

    def center_dropdown(self):
        self.first_tile.center()
        self.first_tile.text_rect.centerx = self.first_tile.rect.centerx
        self.first_tile.text_rect.centery = self.first_tile.rect.centery
        top = self.first_tile.rect.top
        centerx = self.first_tile.rect.centerx
        for surface in self.dropdown_surfaces:
            surface.rect.centerx = centerx
            surface.rect.top = top
            surface.center()

    def mark_clicked(self, clicked_surface):
        self.active = not self.active
        self.dropdown_surfaces.insert(0, self.first_tile)
        self.dropdown_surfaces.pop(self.dropdown_surfaces.index(clicked_surface))
        self.first_tile = clicked_surface

    def blit(self):
        self.first_tile.blit()
        if self.active:
            for surface in self.dropdown_surfaces:
                surface.blit()

    def resize(self):
        self.first_tile.resize()
        for surface in self.dropdown_surfaces:
            surface.resize()
