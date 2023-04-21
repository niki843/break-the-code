from client.game_objects.tiles.plain_text_box import PlainTextTile
from client.game_objects.tiles.toggle_tile import ToggleTile


class GameSessionTile(ToggleTile):
    def __init__(
        self,
        tile_name,
        next_tile_name,
        surface,
        screen,
        size_percent,
        text_size_percent,
        next_surface,
        active_players,
        player_id_usernames_map,
        game_session_id,
        game_session_name="Unknown",
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        ToggleTile.__init__(
            self,
            tile_name,
            next_tile_name,
            surface,
            screen,
            size_percent,
            next_surface,
            tile_addition_width_percent=tile_addition_width_percent,
            tile_addition_height_percent=tile_addition_height_percent,
        )
        self.player_id_usernames_map = player_id_usernames_map
        self.active_players = active_players
        self.game_session_name = game_session_name
        self.game_session_id = game_session_id
        self.player_usernames = list(player_id_usernames_map.values())

        self.text_box = PlainTextTile(
            "game_session_name",
            surface,
            screen,
            size_percent,
            game_session_name,
            text_size_percent,
            20,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )

    def update_players(self, players_id_name_map):
        self.player_id_usernames_map = players_id_name_map
        self.active_players = len(players_id_name_map.keys())
        self.player_usernames = list(players_id_name_map.values())

    def remove_player(self, player_id):
        self.active_players -= 1
        player_username = self.player_id_usernames_map.pop(player_id)
        self.player_usernames.remove(player_username)

    def add_player(self, player_id, player_name):
        self.active_players += 1
        self.player_id_usernames_map[player_id] = player_name
        self.player_usernames.append(player_name)

    def center_text(self):
        self.text_box.text_rect.left = self.rect.left + (self.screen.get_width() * 0.01)
        self.text_box.text_rect.centery = self.rect.centery

    def resize(self):
        super().resize()
        if hasattr(self, "text_box"):
            self.text_box.resize()
