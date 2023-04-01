from client.game_objects.tiles.tile import Tile


class Dropdown(Tile):
    def __init__(
        self,
        first_tile_name,
        first_tile_surface,
        dropdown_name_surface_map,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
    ):
        super().__init__(
            first_tile_name,
            first_tile_surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.dropdown_surfaces = []

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
