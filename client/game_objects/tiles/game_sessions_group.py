from collections import OrderedDict

from client.game_objects.tiles.game_session_tile import GameSessionTile
from client.game_objects.tiles.slider import Slider
from client.utils import common


class GameSessionsGroup:
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
        max_game_sessions_to_display: int,
        first_element_left_location,
        first_element_top_location,
    ):
        self.tile_name = tile_name
        self.next_tile_name = next_tile_name
        self.surface = surface
        self.screen = screen
        self.size_percent = size_percent
        self.text_size_percent = text_size_percent
        self.tile_addition_width = tile_addition_width
        self.tile_addition_height = tile_addition_height
        self.next_surface = next_surface
        self.max_game_sessions_to_display = max_game_sessions_to_display
        self.start_line = 0

        self.first_element_left_location = first_element_left_location
        self.first_element_top_location = first_element_top_location

        self.game_sessions_by_id = OrderedDict()
        self.game_sessions = []

        self.slider = Slider(
            "game_sessions_slider",
            common.get_image("slider_vertical.png"),
            screen,
            size_percent,
            0,
            0,
            "game_session_slider_handle",
            common.get_image("slider_button.png"),
            size_percent,
            0,
            0,
            False,
        )

    def add_game_session(
        self, active_players, player_usernames, game_id, game_session_name
    ):
        game_session = GameSessionTile(
            self.tile_name,
            self.next_surface,
            self.surface,
            self.screen,
            self.size_percent,
            self.text_size_percent,
            self.tile_addition_width,
            self.tile_addition_height,
            self.next_surface,
            active_players,
            player_usernames,
            game_id,
            game_session_name,
        )

        self.game_sessions[game_id] = game_session
        self.game_sessions.append(game_session)
        self.center_last_element()

    def delete_game_session(self, game_session_id):
        del self.game_sessions_by_id[game_session_id]
        self.center_elements()

    def center_elements(self):
        for i in range(self.start_line, self.start_line + self.max_game_sessions_to_display):
            if i >= len(self.game_sessions):
                return

            if i == self.start_line:
                self.game_sessions[i].rect.left = self.first_element_left_location
                self.game_sessions[i].rect.top = self.first_element_top_location
                continue

            self. game_sessions[i].rect.left = self.game_sessions[i-1].rect.left
            self.game_sessions[i].rect.top = self.game_sessions[i-1].rect.bottom + (
                self.screen.get_height() * 0.01
            )

    def center_last_element(self):
        left = self.first_element_left_location
        top = self.first_element_top_location
        if len(self.game_sessions) > 1:
            left = self.game_sessions[len(self.game_sessions) - 3].rect.left
            top = self.game_sessions[len(self.game_sessions) - 3].rect.bottom + (
                self.screen.get_height() * 0.01
            )

        self.game_sessions[len(self.game_sessions) - 2].rect.left = left
        self.game_sessions[len(self.game_sessions) - 2].rect.top = top

    def update_players_count(self, game_session_id, count):
        self.game_sessions_by_id.get(game_session_id).active_players = count

    def scroll_down(self):
        self.change_line(1)

    def scroll_up(self):
        self.change_line(2)

    def change_line(self, index):
        self.start_line += index

        if (
            self.max_game_sessions_to_display + self.start_line > len(self.game_sessions)
            or self.start_line < 0
        ):
            self.start_line -= index
            return

        self.center_elements()

    def blit(self):
        for i in range(self.start_line, self.start_line + self.max_game_sessions_to_display):
            if i >= len(self.game_sessions):
                return
            self.screen.blit(self.game_sessions[i].image, self.game_sessions[i].rect)

        self.screen.blit(self.slider.image, self.slider.rect)
        self.screen.blit(self.slider.slider_handle.image, self.slider.slider_handle.rect)
