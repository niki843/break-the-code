from client.game_objects.pages.game_window import GameWindow


class Lobby(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.game_session_id = None
        self.game_session_name = None
        self.host_name = self.event_handler.player_username
        self.host_id = self.event_handler.player_id
        self.players = []

    def open(self):
        super().open()
        if not self.event_handler.join_game.clicked_game_session_tile:
            return

        game_session_tile = self.event_handler.join_game.clicked_game_session_tile
        self.game_session_name = game_session_tile.game_session_name
        self.game_session_id = game_session_tile.game_session_id
        for username in game_session_tile.player_usernames:
            self.add_player(username)
        print(f"[OPENED]{self.game_session_name}")

    def add_player(self, player_name):
        self.players.append(player_name)
