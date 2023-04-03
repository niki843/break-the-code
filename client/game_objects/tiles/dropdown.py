from client.game_objects.tiles.plain_text_box import PlainTextTile
from client.game_objects.tiles.tile import Tile
from client.utils import common


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
        self.first_tile.priority = 1

        self.dropdown_arrow = Tile(
            "dropdown_arrow",
            common.get_image("dropdown.png"),
            screen,
            size_percent - 6,
            0,
            0,
        )

        self.dropdown_surfaces = []
        self.active = False
        self.screen = screen

        for name, text in dropdown_name_text_map.items():
            tile = self.create_dropdown_tile(
                name,
                screen,
                surface,
                size_percent,
                tile_addition_width,
                tile_addition_height,
                text,
            )
            tile.priority = 1
            self.dropdown_surfaces.append(tile)

    def create_dropdown_tile(
        self,
        name,
        screen,
        surface,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        first_tile_text,
    ):
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
        self.first_tile.text_rect.left = self.first_tile.rect.left + (
            self.screen.get_width() * 0.022
        )
        self.first_tile.text_rect.centery = self.first_tile.rect.centery
        top = self.first_tile.rect.bottom
        centerx = self.first_tile.rect.centerx
        for surface in self.dropdown_surfaces:
            surface.rect.top = top
            surface.rect.centerx = centerx
            surface.text_rect.centerx = surface.rect.centerx
            surface.text_rect.centery = surface.rect.centery

        self.dropdown_arrow.rect.right = self.first_tile.rect.right - (
            self.screen.get_width() * 0.004
        )
        self.dropdown_arrow.rect.centery = self.first_tile.rect.centery

    def drop_elements(self):
        self.active = not self.active

    def mark_clicked(self, clicked_surface):
        clicked_surface.rect.centerx = self.first_tile.rect.centerx
        clicked_surface.rect.centery = self.first_tile.rect.centery
        self.dropdown_surfaces.insert(0, self.first_tile)
        self.dropdown_surfaces.pop(self.dropdown_surfaces.index(clicked_surface))
        self.first_tile = clicked_surface
        self.center_dropdown()

    def blit(self):
        self.first_tile.blit()
        self.screen.blit(self.dropdown_arrow.image, self.dropdown_arrow.rect)
        if self.active:
            for surface in self.dropdown_surfaces:
                surface.blit()

    def resize(self):
        self.first_tile.resize()
        self.dropdown_arrow.resize()
        for surface in self.dropdown_surfaces:
            surface.resize()

