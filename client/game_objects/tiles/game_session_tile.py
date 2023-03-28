from client.game_objects.tiles.toggle_tile import ToggleTile


class GameSessionTile(ToggleTile):

    def __init__(
        self,
        name_id,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        active_players,
        player_usernames,
    ):
        ToggleTile.__init__(
            self,
            name_id,
            name_id,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
        )

        self.active_players = active_players
        self.player_usernames = player_usernames
