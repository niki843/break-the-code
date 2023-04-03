from client.game_objects.custom_exceptions.game_sessionId_not_provided_exception import (
    GameSessionIdNotProvidedException,
)
from client.game_objects.custom_exceptions.player_usernames_not_provided_exception import (
    PlayerUsernamesNotProvidedException,
)
from client.game_objects.pages.game_window import GameWindow


class Lobby(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.game_session_id = None
        self.game_session_name = None
        self.host_name = self.event_handler.server_communication_manager.player_username
        self.host_id = self.event_handler.server_communication_manager.player_id
        self.players_id_username_map = []

        self.build()

    def build(self):
        # This order is important and should not change
        self.build_clear_background()

        self.build_back_tile()

        self.build_tiles_background()
        self.build_game_info_box()

    def resize(self):
        super().resize()
        self.set_back_tile()
        self.set_tiles_background_size()
        self.set_game_info_size()

    def open(self, **kwargs):
        super().open()
        if kwargs.get("create_game"):
            self.players_id_username_map = {
                self.event_handler.server_communication_manager.player_username: self.event_handler.server_communication_manager.player_id
            }
            self.game_session_name = kwargs.get("game_name") or "Unknown"

            self.event_handler.server_communication_manager.send_create_game_message(
                self.game_session_name
            )
        else:
            self.players_id_username_map = kwargs.get("player_id_usernames_map")
            self.game_session_id = kwargs.get("game_session_id")

            if not self.game_session_id:
                raise GameSessionIdNotProvidedException()
            if not self.players_id_username_map:
                raise PlayerUsernamesNotProvidedException()

            self.event_handler.server_communication_manager.send_join_game_message(
                self.game_session_id
            )

        print(f"[OPENED]{self.game_session_name}")

    def add_player(self, player_id, player_name):
        self.players_id_username_map[player_id] = player_name

    def close(self):
        self.event_handler.server_communication_manager.send_exit_game_message()

    def activate_tile(self, tile, event):
        if tile.name == self.back_tile.name:
            self.close()
            self.event_handler.menu.open()

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)
        self.event_handler.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )
        self.game_info_box.blit()
