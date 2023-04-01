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
        tile_addition_width,
        tile_addition_height,
        next_surface,
        active_players,
        player_usernames,
        game_session_id,
        game_session_name="Unknown",
    ):
        ToggleTile.__init__(
            self,
            tile_name,
            next_tile_name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
        )
        self.player_usernames = player_usernames
        self.active_players = active_players
        self.game_session_name = game_session_name
        self.game_session_id = game_session_id

        self.text_box = PlainTextTile(
            "game_session_name",
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            game_session_name,
            text_size_percent,
            20,
        )

    def update_players(self, players_id_name_map):
        self.active_players = len(players_id_name_map.keys())
        self.player_usernames = players_id_name_map.values()

    def center_text(self):
        self.text_box.text_rect.left = self.rect.left + (self.screen.get_width() * 0.01)
        self.text_box.text_rect.centery = self.rect.centery

    def resize(self):
        super().resize()
        if hasattr(self, "text_box"):
            self.text_box.resize()
