from client.game_objects.tiles.toggle_tile import ToggleTile


class GameSessionTile(ToggleTile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        active_players,
        player_usernames,
        id,
    ):
        ToggleTile.__init__(
            self,
            name,
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
        )

        self.id = id
        self.active_players = active_players
        self.player_usernames = player_usernames

    def update_players(self, players_id_name_map):
        self.active_players = len(players_id_name_map.keys())
        self.player_usernames = players_id_name_map.values()
