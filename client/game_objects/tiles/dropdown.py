from client.game_objects.tiles.tile import Tile


class Dropdown:
    def __init__(
        self,
        first_tile_name,
        first_tile_surface,
        dropdown_name_surface_map,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        left_position,
        top_position,
    ):
        self.first_tile = Tile(
            first_tile_name,
            first_tile_surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.dropdown_surfaces = []
        self.active = False
        self.first_tile.rect.left = left_position
        self.first_tile.rect.top = top_position
        self.screen = screen

        for name, surface in dropdown_name_surface_map.items():
            self.dropdown_surfaces.append(
                Tile(
                    name,
                    surface,
                    screen,
                    size_percent,
                    tile_addition_width,
                    tile_addition_height,
                )
            )

    def center_dropdown(self):
        left = self.first_tile.rect.left
        top = self.first_tile.rect.bottom
        for surface in self.dropdown_surfaces:
            surface.rect.left = left
            surface.rect.top = top
            top = surface.rect.bottom

    def mark_clicked(self, clicked_surface):
        self.active = not self.active
        self.dropdown_surfaces.insert(0, self.first_tile)
        self.dropdown_surfaces.pop(self.dropdown_surfaces.index(clicked_surface))
        self.first_tile = clicked_surface

    def blit(self):
        self.screen.blit(self.first_tile.image, self.first_tile.rect)
        if self.active:
            for surface in self.dropdown_surfaces:
                self.screen.blit(surface.image, surface.rect)

    def resize(self):
        self.first_tile.resize()
        for surface in self.dropdown_surfaces:
            surface.resize()
