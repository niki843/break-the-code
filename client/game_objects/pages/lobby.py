from client.game_objects.pages.game_window import GameWindow


class Lobby(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.game_session_id = None
        self.game_session_name = None
        self.host_name = self.event_handler.server_communication_manager.player_username
        self.host_id = self.event_handler.server_communication_manager.player_id
        self.players = []

    def open(self, **kwargs):
        super().open()

        self.game_session_name = kwargs.get("game_name") or "Unknown"
        self.players = kwargs.get("player_usernames") or [self.event_handler.server_communication_manager.player_username]

        print(f"[OPENED]{self.game_session_name}")

    def add_player(self, player_name):
        self.players.append(player_name)
