from copy import copy

import client
from client.custom_exceptions.game_sessionId_not_provided_exception import (
    GameSessionIdNotProvidedException,
)
from client.custom_exceptions.player_not_found_exception import (
    PlayerNotFoundException,
)
from client.custom_exceptions.player_usernames_not_provided_exception import (
    PlayerUsernamesNotProvidedException,
)
from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common


class Lobby(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.game_session_id = None
        self.game_session_name = None
        self.players_id_username_map = {}

        self.start_game_tile = None

        self.player_info_group = None

        self.build()

    def build(self):
        # This order is important and should not change
        self.build_clear_background()

        self.build_back_tile()

        self.build_tiles_background()
        self.build_game_info_box()

        self.build_player_info_group()

        self.build_start_game_tile()

    def resize(self):
        super().resize()
        self.set_back_tile()
        self.set_tiles_background_size()
        self.set_game_info_size()
        self.set_player_info_group_size()
        self.set_start_game_tile()

    def build_start_game_tile(self):
        surface = common.get_image("start_1.png")
        next_surface = common.get_image("start_1_pressed.png")
        self.start_game_tile = ToggleTile(
            "start_game",
            "start_game",
            surface,
            client.state_manager.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            0,
            0,
            next_surface,
            shrink_percent=1,
        )

        self.set_start_game_tile()

    def set_start_game_tile(self):
        if not self.start_game_tile:
            return

        self.start_game_tile.resize()
        self.start_game_tile.rect.right = client.state_manager.screen_rect.right - (
            client.state_manager.screen.get_width() * 0.03
        )
        self.start_game_tile.rect.bottom = client.state_manager.screen_rect.bottom - (
            client.state_manager.screen.get_height() * 0.03
        )

    def open(self, **kwargs):
        super().open()
        if kwargs.get("create_game"):
            self.game_session_name = kwargs.get("game_name") or "Unknown"

            client.server_communication_manager.send_create_game_message(
                self.game_session_name
            )

            client.state_manager.set_host(
                client.state_manager.player_id, client.state_manager.username
            )

            self.add_player(
                client.state_manager.host_id, client.state_manager.host_username
            )
            self.tiles_group.add(self.start_game_tile)
        else:
            self.players_id_username_map = kwargs.get("player_id_usernames_map")
            self.game_session_id = kwargs.get("game_session_id")
            self.game_session_name = kwargs.get("game_session_name")

            client.state_manager.set_host(
                list(self.players_id_username_map.values())[0],
                list(self.players_id_username_map.keys())[0],
            )

            if not self.game_session_id:
                raise GameSessionIdNotProvidedException()
            if not self.players_id_username_map:
                raise PlayerUsernamesNotProvidedException()

            client.server_communication_manager.send_join_game_message(
                self.game_session_id
            )
            self.add_player(
                client.state_manager.player_id, client.state_manager.username
            )
            self.players_id_username_map.update(
                self.player_info_group.get_player_name_id_map()
            )

    def add_player(self, player_id, player_name):
        self.players_id_username_map[player_id] = player_name
        self.player_info_group.add_player_tile(player_id, player_name)

    def update_game_session_id(self, game_session_id):
        self.game_session_id = game_session_id

    def set_player_info_group(self, player_info_group):
        self.player_info_group = player_info_group
        self.set_player_info_group_size()

    def close(self):
        self.player_info_group.clear_players()

    def replace_host(self, player_id):
        self.set_player_disconnected(client.state_manager.host_id)
        client.state_manager.set_host(
            player_id, self.players_id_username_map.get(player_id)
        )

        if client.state_manager.am_i_host():
            self.tiles_group.add(self.start_game_tile)

        if not client.state_manager.host_username:
            raise PlayerNotFoundException()

    def set_player_disconnected(self, player_id):
        self.player_info_group.remove_player(
            self.players_id_username_map.get(player_id)
        )
        self.players_id_username_map.pop(player_id)

    def start_game(self):
        player_info_group = copy(self.player_info_group)
        self.close()
        self.event_handler.new_game.open(
            player_info_group=player_info_group,
        )

    def activate_tile(self, tile, event):
        if tile.name == self.back_tile.name:
            client.server_communication_manager.send_exit_game_message()
            self.close()
            self.event_handler.menu.open()
        if (
            tile.name == self.start_game_tile.name
            and client.state_manager.am_i_host()
            and len(self.players_id_username_map.keys()) >= 3
        ):
            self.start_game()

    def blit(self):
        super().blit()
        client.state_manager.screen.blit(self.back_tile.image, self.back_tile.rect)
        client.state_manager.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )
        self.game_info_box.blit()
        self.player_info_group.blit()

        if client.state_manager.am_i_host():
            client.state_manager.screen.blit(
                self.start_game_tile.image, self.start_game_tile.rect
            )
