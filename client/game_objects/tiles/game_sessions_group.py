from collections import OrderedDict

import pygame

from client.game_objects.tiles.game_session_tile import GameSessionTile
from client.game_objects.tiles.slider import Slider
from client.game_objects.tiles.tile import Tile
from client.utils import common


class GameSessionsGroup(Tile):
    def __init__(
        self,
        group_name,
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
        slider_position_right,
        last_element_bottom_position,
    ):
        transparent_background = pygame.Surface(
            [
                slider_position_right - first_element_left_location,
                last_element_bottom_position - first_element_top_location,
            ],
            pygame.SRCALPHA,
            32,
        )
        transparent_background = transparent_background.convert_alpha()

        super().__init__(
            group_name,
            transparent_background,
            screen,
            47.4,
            0,
            0,
        )
        self.rect.left = first_element_left_location
        self.rect.top = first_element_top_location

        self.tile_name = tile_name
        self.next_tile_name = next_tile_name
        self.tile_addition_width = tile_addition_width
        self.tile_addition_height = tile_addition_height
        self.size_percent = size_percent
        self.screen = screen
        self.text_size_percent = text_size_percent
        self.game_session_tile_surface = surface
        self.next_surface = next_surface
        self.max_game_sessions_to_display = max_game_sessions_to_display
        self.start_line = 0

        self.first_element_left_location = first_element_left_location
        self.first_element_top_location = first_element_top_location
        self.slider_position_right = slider_position_right

        self.game_sessions_by_id = OrderedDict()
        self.game_sessions = []

        self.slider = Slider(
            "game_sessions_slider",
            common.get_image("slider_vertical.png"),
            screen,
            1.4,
            0,
            -300,
            "game_session_slider_handle",
            common.get_image("slider_button.png"),
            1.4,
            0,
            0,
            False,
        )
        self.position_slider()
        self.slider.update()

    def add_game_session(
        self, active_players, player_usernames, game_id, game_session_name
    ):
        game_session = GameSessionTile(
            self.tile_name,
            self.next_tile_name,
            self.game_session_tile_surface,
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

        self.game_sessions_by_id[game_id] = game_session
        self.game_sessions.append(game_session)
        self.center_last_element()
        self.slider.update(delimiters=len(self.game_sessions) - self.max_game_sessions_to_display + 1)

        return game_session

    def delete_game_session(self, game_session_id):
        current_game_session_index = list(self.game_sessions_by_id.keys()).index(game_session_id)
        self.game_sessions.pop(current_game_session_index)
        del self.game_sessions_by_id[game_session_id]
        self.start_line -= 1 if self.start_line > 0 else 0
        self.center_elements()
        self.slider.handle_position -= 1
        self.slider.update(delimiters=len(self.game_sessions) - self.max_game_sessions_to_display + 1)

    def center_elements(self):
        for i in range(
            self.start_line, self.start_line + self.max_game_sessions_to_display
        ):
            if i >= len(self.game_sessions):
                return

            if i == self.start_line:
                self.game_sessions[i].rect.left = self.first_element_left_location
                self.game_sessions[i].rect.top = self.first_element_top_location
                self.game_sessions[i].center_text()
                continue

            self.game_sessions[i].rect.left = self.game_sessions[i - 1].rect.left
            self.game_sessions[i].rect.top = self.game_sessions[i - 1].rect.bottom
            self.game_sessions[i].center_text()

            # Try to move the last element out of screen to remove collision issues
            try:
                self.game_sessions[i+1].rect.top = self.screen.get_rect().bottom
            except IndexError:
                pass

    def center_last_element(self):
        if not self.game_sessions:
            return

        left = self.first_element_left_location
        top = self.first_element_top_location
        if len(self.game_sessions) > 1:
            left = self.game_sessions[len(self.game_sessions) - 2].rect.left
            top = self.game_sessions[len(self.game_sessions) - 2].rect.bottom

        self.game_sessions[len(self.game_sessions) - 1].rect.left = left
        self.game_sessions[len(self.game_sessions) - 1].rect.top = top
        self.game_sessions[len(self.game_sessions) - 1].center_text()

    def position_slider(self):
        self.slider.rect.left = self.slider_position_right
        self.slider.rect.top = self.first_element_top_location
        self.slider.set_slider_handle_position()

    def update_players_count(self, game_session_id, count):
        self.game_sessions_by_id.get(game_session_id).active_players = count

    def scroll_down(self):
        self.change_line(1)

    def scroll_up(self):
        self.change_line(-1)

    def change_line(self, index):
        self.start_line += index

        if (
            self.max_game_sessions_to_display + self.start_line
            > len(self.game_sessions)
            or self.start_line < 0
        ):
            self.start_line -= index
            return

        self.center_elements()

    def tile_exists(self, game_session_id):
        return game_session_id in self.game_sessions_by_id

    def blit(self):
        self.screen.blit(self.image, self.rect)
        for i in range(
            self.start_line, self.start_line + self.max_game_sessions_to_display
        ):
            if i >= len(self.game_sessions):
                # TODO: Or not TODO that is the question, aka should we replace this with return and
                #  not have a scroll when the items are bellow max_game_sessions_to_display
                continue
            self.screen.blit(self.game_sessions[i].image, self.game_sessions[i].rect)
            self.screen.blit(
                self.game_sessions[i].text_box.text_surface,
                self.game_sessions[i].text_box.text_rect,
            )

        self.screen.blit(self.slider.image, self.slider.rect)
        self.screen.blit(
            self.slider.slider_handle.image, self.slider.slider_handle.rect
        )
