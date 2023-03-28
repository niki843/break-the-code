from client.game_objects.tiles.toggle_tile import ToggleTile


class GameSessionTile(ToggleTile):

    def __init__(
        self,
        name,
        next_name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        active_players,
    ):
        ToggleTile.__init__(
            self,
            name,
            next_name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
        )

        self.active_players = active_players