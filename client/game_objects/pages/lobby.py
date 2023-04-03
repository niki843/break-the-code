from client.game_objects.custom_exceptions.game_sessionId_not_provided_exception import (
    GameSessionIdNotProvidedException,
)
from client.game_objects.custom_exceptions.player_usernames_not_provided_exception import (
    PlayerUsernamesNotProvidedException,
)
from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.player_info_group import PlayerInfoGroup


class Lobby(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.game_session_id = None
        self.game_session_name = None
        self.host_name = None
        self.host_id = None
        self.players_id_username_map = []

        self.player_info_group = None

        self.build()

    def build(self):
        # This order is important and should not change
        self.build_clear_background()

        self.build_back_tile()

        self.build_tiles_background()
        self.build_game_info_box()

        self.build_player_info_group()

    def resize(self):
        super().resize()
        self.set_back_tile()
        self.set_tiles_background_size()
        self.set_game_info_size()
        self.set_player_info_group_size()

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

            self.host_id = self.event_handler.server_communication_manager.player_id
            self.host_name = self.event_handler.server_communication_manager.player_username

            self.players_id_username_map[self.host_id] = self.host_name
        else:
            self.players_id_username_map = kwargs.get("player_id_usernames_map")
            self.game_session_id = kwargs.get("game_session_id")
            self.game_session_name = kwargs.get("game_session_name")

            self.host_id = list(self.players_id_username_map.keys())[0]
            self.host_name = list(self.players_id_username_map.values())[0]

            if not self.game_session_id:
                raise GameSessionIdNotProvidedException()
            if not self.players_id_username_map:
                raise PlayerUsernamesNotProvidedException()

            self.event_handler.server_communication_manager.send_join_game_message(
                self.game_session_id
            )

    def add_player(self, player_id, player_name):
        self.players_id_username_map[player_id] = player_name

    def update_game_session_id(self, game_session_id):
        self.game_session_id = game_session_id

    def set_player_info_group(self, player_info_group):
        self.player_info_group = player_info_group
        self.set_player_info_group_size()

    def close(self):
        self.event_handler.server_communication_manager.send_exit_game_message()
        self.player_info_group.clear_players()

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
        self.player_info_group.blit()
