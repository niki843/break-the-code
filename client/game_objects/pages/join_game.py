import asyncio
import copy
from collections import OrderedDict

import client
from client.game_objects.groups.game_sessions_group import GameSessionsGroup
from client.utils import common

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None

        self.scroll_text_tile = None

        self.game_info_tile = None
        self.game_info_box = None

        self.game_session_tiles = OrderedDict()
        self.clicked_game_session_tile = None

        self.game_session_group = None

        self.build()

    def build(self):
        self.build_clear_background()

        self.build_tiles_background()

        self.build_back_tile()

        self.build_game_info_label()
        self.build_game_info_box()

        self.build_game_sessions_group()

        self.build_player_info_group()

        self.build_join_game_button()

    def resize(self):
        super().resize()
        self.set_tiles_background_size()

        self.set_back_tile()

        self.set_game_info_label_size()
        self.set_game_info_size()

        self.set_game_sessions_group_size()
        self.set_player_info_group_size()

        self.set_join_game_button_size()

    def build_join_game_button(self):
        surface = common.get_image("join_game.png")

        self.join_game_tile = Tile(
            "join_game_button",
            surface,
            client.state_manager.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            0.01,
        )

        self.tiles_group.add(self.join_game_tile)
        self.set_join_game_button_size()

    def set_join_game_button_size(self):
        if not self.join_game_tile:
            return

        self.join_game_tile.resize()
        self.join_game_tile.rect.right = client.state_manager.screen_rect.right - (
            client.state_manager.screen.get_width() * 0.03
        )
        self.join_game_tile.rect.bottom = client.state_manager.screen_rect.bottom - (
            client.state_manager.screen.get_height() * 0.03
        )

    def build_game_info_label(self):
        surface = common.get_image("game_info.png")
        self.game_info_tile = Tile(
            name="game_info",
            surface=surface,
            screen=client.state_manager.screen,
            size_percent=25,
        )

        self.set_game_info_label_size()

    def set_game_info_label_size(self):
        if not self.game_info_tile:
            return

        self.game_info_tile.resize()
        self.game_info_tile.rect.top = self.tiles_background.rect.top + (
            client.state_manager.screen.get_height() * 0.03
        )
        self.game_info_tile.rect.right = self.tiles_background.rect.right - (
            client.state_manager.screen.get_width() * 0.06
        )

    def set_game_info_size(self):
        if not self.game_info_box:
            return

        self.game_info_box.resize()
        self.game_info_box.rect.bottom = self.tiles_background.rect.bottom - (
            client.state_manager.screen.get_height() * 0.04
        )
        self.game_info_box.rect.centerx = self.game_info_tile.rect.centerx

    def build_game_sessions_group(self):
        left, top, right = self.get_game_sessions_group_position()

        self.game_session_group = GameSessionsGroup(
            "game_session_group",
            "game_session_tile",
            "game_session_tile",
            common.get_image("game_session.png"),
            client.state_manager.screen,
            44,
            40,
            common.get_image("game_session_selected.png"),
            6,
            left,
            top,
            right,
        )

        self.tiles_group.add(self.game_session_group)
        self.tiles_group.add(self.game_session_group.slider)
        self.tiles_group.add(self.game_session_group.slider.slider_handle)

    def update_game_sessions(self, game_sessions, **kwargs):
        self.game_session_group.clear()
        for game_session_id, game_session in game_sessions.items():
            game_session = self.game_session_group.add_game_session(
                active_players=game_session.get("connected_players"),
                player_id_usernames_map=game_session.get("player_id_name_map"),
                game_id=game_session_id,
                game_session_name=game_session.get("room_name"),
            )
            game_session.priority = 1
        self.tiles_group.add(self.game_session_group.shown_game_sessions)

    def add_game_session_id(self, game_session_id, game_session_name, host_id, host_name, **kwargs):
        game_session = self.game_session_group.add_game_session(
            active_players=1,
            player_id_usernames_map={host_id: host_name},
            game_id=game_session_id,
            game_session_name=game_session_name,
        )
        game_session.priority = 1
        self.tiles_group.add(self.game_session_group.shown_game_sessions)

    def remove_game_session(self, game_session_id, **kwargs):
        self.tiles_group.remove(
            self.game_session_group.game_sessions_by_id.get(game_session_id)
        )
        self.game_session_group.delete_game_session(game_session_id)
        self.tiles_group.add(self.game_session_group.shown_game_sessions)

    def add_player(self, game_session_id, player_id, player_name, **kwargs):
        if self.clicked_game_session_tile.game_session_id == game_session_id:
            self.player_info_group.add_player_tile(player_id, player_name)

        self.game_session_group.add_player(game_session_id, player_id, player_name)

    def remove_player(self, game_session_id, player_id, **kwargs):
        if self.clicked_game_session_tile.game_session_id == game_session_id:
            player_name = self.player_info_group.get_player_name_id_map().get(player_id)
            self.player_info_group.remove_player(player_name)

        self.game_session_group.remove_player(game_session_id, player_id)

    def set_game_sessions_group_size(self):
        self.game_session_group.resize()
        left, top, right = self.get_game_sessions_group_position()
        self.game_session_group.update_initial_position(left, top, right)
        self.game_session_group.center_elements()
        self.game_session_group.position_slider()

    def get_game_sessions_group_position(self):
        left = self.tiles_background.rect.left + (
            client.state_manager.screen.get_width() * 0.02
        )
        top = self.tiles_background.rect.top + (
            client.state_manager.screen.get_height() * 0.03
        )
        right = self.game_info_box.rect.left - (
            client.state_manager.screen.get_width() * 0.016
        )
        return left, top, right

    def blit(self):
        super().blit()
        client.state_manager.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )

        client.state_manager.screen.blit(self.back_tile.image, self.back_tile.rect)
        client.state_manager.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )

        client.state_manager.screen.blit(
            self.game_info_tile.image, self.game_info_tile.rect
        )

        client.state_manager.screen.blit(self.game_info_box.image, self.game_info_box.rect)

        self.game_session_group.blit()

        self.player_info_group.blit()

    def open(self):
        super().open()
        client.server_communication_manager.get_current_game()

    def close(self):
        client.server_communication_manager.exit_get_current_games_state()

        if self.clicked_game_session_tile:
            self.clicked_game_session_tile.next_value()
            self.reset_selected_game_session()

        for game_session in self.game_session_group.game_sessions:
            self.tiles_group.remove(game_session)

    def activate_tile(self, tile, event):
        match event.button:
            case client.LEFT_BUTTON_CLICK:
                self.tile_left_button_click_event(tile)
            case client.SCROLL_UP:
                self.tile_scroll_up_event(tile)
            case client.SCROLL_DOWN:
                self.tile_scroll_down_event(tile)

    def tile_left_button_click_event(self, tile):
        match tile.name:
            case self.back_tile.name:
                self.event_handler.menu.open()
                self.close()
            case self.game_session_group.slider.slider_handle.name:
                self.event_handler.handle_slider_clicked(self.scroll_text_tile)
            case self.game_session_group.tile_name:
                self.player_info_group.clear_players()

                if self.clicked_game_session_tile:
                    self.clicked_game_session_tile.next_value()

                if self.clicked_game_session_tile == tile:
                    self.clicked_game_session_tile = None
                    return

                self.clicked_game_session_tile = tile
                tile.next_value()
                for player_id, player_name in tile.player_id_usernames_map.items():
                    self.player_info_group.add_player_tile(player_id, player_name)
            case self.join_game_tile.name:
                if (
                    not self.clicked_game_session_tile
                    or self.clicked_game_session_tile.active_players >= 4
                ):
                    return

                # Keeping it as a different variable because it will get reset when we call the close function
                clicked_game_session_tile = self.clicked_game_session_tile
                player_info_group = copy.copy(self.player_info_group)

                # calling close before anything else to stop the automated server call for refreshing game sessions
                self.close()

                self.event_handler.lobby.set_player_info_group(player_info_group)
                self.event_handler.lobby.open(
                    game_session_id=clicked_game_session_tile.game_session_id,
                    player_id_usernames_map=clicked_game_session_tile.player_id_usernames_map,
                    game_session_name=clicked_game_session_tile.game_session_name,
                )

    def tile_scroll_up_event(self, tile):
        match tile.name:
            case self.game_session_group.name | self.game_session_group.tile_name \
                 | self.game_session_group.next_tile_name | self.game_session_group.slider.name \
                 | self.game_session_group.slider.slider_handle.name:
                # Scroll up the game sessions group
                self.game_session_group.slider.previous_handle_position()
                self.game_session_group.scroll_up()

    def tile_scroll_down_event(self, tile):
        match tile.name:
            case self.game_session_group.name | self.game_session_group.tile_name \
                 | self.game_session_group.next_tile_name | self.game_session_group.slider.name \
                 | self.game_session_group.slider.slider_handle.name:
                # Scroll down the game sessions group
                self.game_session_group.slider.next_handle_position()
                self.game_session_group.scroll_down()
                self.tiles_group.add(self.game_session_group.shown_game_sessions[-1])

    def reset_selected_game_session(self):
        if self.clicked_game_session_tile:
            self.clicked_game_session_tile = None
            self.player_info_group.clear_players()
