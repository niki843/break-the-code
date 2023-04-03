from pygame import Color

import client
import pygame

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.dropdown import Dropdown
from client.game_objects.tiles.input_box_tile import InputBoxTile
from client.game_objects.tiles.plain_text_box import PlainTextTile
from client.game_objects.tiles.tile import Tile
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common


class Menu(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.new_game_tile = None
        self.join_game_tile = None
        self.settings_tile = None
        self.quit_tile = None

        self.blured_tile = None
        self.game_session_name_box = None
        self.game_session_name_text = None
        self.number_players_dropdown = None
        self.cancel_button = None
        self.create_button = None
        self.private_game_toggle_button = None
        self.number_players_label = None
        self.private_game_label = None

        self.is_private_game = False
        self.game_session_name = ""
        self.players_count = "4"

        self.build()

    def build(self):
        # This order is important and should not change
        super().build()
        self.build_join_game()
        self.build_new_game()
        self.build_settings()
        self.build_quit_game()

    def resize(self):
        super().resize()
        self.set_join_game_size()
        self.set_new_game_size()
        self.set_settings_size()
        self.set_quit_game_size()

        self.set_blurred_background_size()
        self.set_game_session_name_box_size()
        self.set_game_name_text_size()
        self.set_cancel_button_size()
        self.set_create_button_size()
        self.set_number_players_label_size()
        self.set_number_players_dropdown_size()
        self.set_toggle_size()
        self.set_private_game_label_size()

    def build_join_game(self):
        surface = common.get_image("join_game.png")
        self.join_game_tile = Tile(
            "join_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_join_game_size()

    def set_join_game_size(self):
        if not self.join_game_tile:
            return

        self.join_game_tile.resize()
        self.join_game_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.join_game_tile.rect.centery = self.event_handler.screen_rect.centery
        self.tiles_group.add(self.join_game_tile)

    def build_new_game(self):
        surface = common.get_image("new_game.png")
        self.new_game_tile = Tile(
            "new_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_new_game_size()

    def set_new_game_size(self):
        if not self.new_game_tile:
            return

        self.new_game_tile.resize()
        self.new_game_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.new_game_tile.rect.bottom = (
            self.join_game_tile.rect.top - client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.new_game_tile)

    def build_settings(self):
        surface = common.get_image("settings.png")
        self.settings_tile = Tile(
            "settings",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_settings_size()

    def set_settings_size(self):
        if not self.settings_tile:
            return

        self.settings_tile.resize()
        self.settings_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.settings_tile.rect.top = (
            self.join_game_tile.rect.bottom + client.BETWEEN_TILES_SPACING
        )
        self.tiles_group.add(self.settings_tile)

    def build_quit_game(self):
        surface = common.get_image("quit.png").convert_alpha()
        self.quit_tile = Tile(
            "quit_game",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
        )
        self.set_quit_game_size()

    def set_quit_game_size(self):
        if not self.quit_tile:
            return

        self.quit_tile.resize()
        self.quit_tile.rect.right = (
            self.event_handler.screen_rect.right
            - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.quit_tile.rect.top = (
            self.event_handler.screen_rect.bottom
            - self.quit_tile.image.get_height()
            - client.BETWEEN_TILE_AND_SCREEN_SPACING
        )
        self.tiles_group.add(self.quit_tile)

    def build_blurred_background(self):
        blurr = common.get_image("blur_bgr.png")
        self.blured_tile = Tile(
            "blurr",
            blurr,
            self.event_handler.screen,
            100,
            0,
            0,
        )

        self.tiles_group.add(self.blured_tile)

        self.set_blurred_background_size()

    def set_blurred_background_size(self):
        if not self.blured_tile:
            return

        self.blured_tile.resize()
        self.blured_tile.rect.centerx = self.event_handler.screen.get_rect().centerx
        self.blured_tile.rect.centery = self.event_handler.screen.get_rect().centery

    def build_game_session_name_box(self):
        surface = common.get_image("create_game_window.png")
        self.game_session_name_box = Tile(
            "game_session_name_box",
            surface,
            self.event_handler.screen,
            55,
            0,
            0,
        )
        # Set it as a higher priority than anything behind
        self.game_session_name_box.priority = 1

        self.set_game_session_name_box_size()

    def set_game_session_name_box_size(self):
        if not self.game_session_name_box:
            return

        self.game_session_name_box.resize()
        self.game_session_name_box.rect.centerx = (
            self.event_handler.screen.get_rect().centerx
        )
        self.game_session_name_box.rect.centery = (
            self.event_handler.screen.get_rect().centery
        )

    def build_game_name_text_box(self):
        surface = common.get_image("non_selected_nickname.png")
        next_surface = common.get_image("selected_nickname.png")

        self.game_session_name_text = InputBoxTile(
            "game_name_input",
            "game_name_input",
            surface,
            self.event_handler.screen,
            43,
            0,
            0,
            next_surface,
            "Game-Name",
            text_size_percentage_from_screen_height=5,
        )

        self.set_game_name_text_size()
        self.tiles_group.add(self.game_session_name_text)

    def set_game_name_text_size(self):
        if not self.game_session_name_text:
            return

        self.game_session_name_text.resize()
        self.game_session_name_text.rect.centerx = (
            self.game_session_name_box.rect.centerx
        )
        self.game_session_name_text.rect.top = self.game_session_name_box.rect.top + (
            self.event_handler.screen.get_height() * 0.1
        )
        self.game_session_name_text.center()

    def build_number_players_label(self):
        transparent_image = common.generate_transparent_image(self.game_session_name_text.image.get_width() - 100, self.game_session_name_text.image.get_height())
        self.number_players_label = PlainTextTile(
            "number_of_players",
            transparent_image,
            self.event_handler.screen,
            40,
            0,
            0,
            "Number of players:",
            45,
            20
        )

        self.set_number_players_label_size()

    def set_number_players_label_size(self):
        if not self.number_players_label:
            return

        self.number_players_label.resize()
        self.number_players_label.rect.left = self.game_session_name_text.rect.left
        self.number_players_label.rect.top = self.game_session_name_text.rect.bottom + (
            self.event_handler.screen.get_height() * 0.03
        )
        self.number_players_label.center()

    def build_number_players_dropdown_box(self):
        surface = common.get_image("player_number_menu.png")
        name_text_map = {
            "players_count": "3"
        }

        self.number_players_dropdown = Dropdown(
            first_tile_name="players_count",
            first_tile_text="4",
            surface=surface,
            dropdown_name_text_map=name_text_map,
            screen=self.event_handler.screen,
            size_percent=9,
            tile_addition_width=0,
            tile_addition_height=0,
        )
        self.players_count_tile = self.number_players_dropdown.first_tile

        self.set_number_players_dropdown_size()
        self.tiles_group.add(self.number_players_dropdown.first_tile)

    def set_number_players_dropdown_size(self):
        if not self.number_players_dropdown:
            return

        self.number_players_dropdown.resize()
        self.number_players_dropdown.first_tile.rect.right = self.game_session_name_text.rect.right
        self.number_players_dropdown.first_tile.rect.top = self.game_session_name_text.rect.bottom + (
            self.event_handler.screen.get_height() * 0.04
        )
        self.number_players_dropdown.center_dropdown()

    def build_private_game_label(self):
        transparent_image = common.generate_transparent_image(self.game_session_name_text.image.get_width() - 100, self.game_session_name_text.image.get_height())
        self.private_game_label = PlainTextTile(
            "private_game",
            transparent_image,
            self.event_handler.screen,
            40,
            0,
            0,
            "Private game:",
            45,
            20
        )

        self.set_private_game_label_size()

    def set_private_game_label_size(self):
        if not self.private_game_label:
            return

        self.private_game_label.resize()
        self.private_game_label.rect.left = self.number_players_label.rect.left
        self.private_game_label.rect.top = self.number_players_label.rect.bottom + (
            self.event_handler.screen.get_height() * 0.03
        )
        self.private_game_label.center()

    def build_private_game_toggle(self):
        surface = common.get_image("toggle_off.png")
        next_surface = common.get_image("toggle_on.png")

        self.private_game_toggle_button = ToggleTile(
            name="toggle_button_off",
            next_name="toggle_button_on",
            current_surface=surface,
            screen=self.event_handler.screen,
            size_percent=8,
            tile_addition_width=0,
            tile_addition_height=0,
            next_surface=next_surface,
            shrink_percent=0,
        )

        self.set_toggle_size()
        self.tiles_group.add(self.private_game_toggle_button)

    def set_toggle_size(self):
        if not self.private_game_toggle_button:
            return

        self.private_game_toggle_button.resize()
        self.private_game_toggle_button.rect.right = (
            self.game_session_name_text.rect.right
        )
        self.private_game_toggle_button.rect.top = (
            self.number_players_dropdown.first_tile.rect.bottom
            + (self.event_handler.screen.get_height() * 0.04)
        )

    def build_cancel_button_tile(self):
        surface = common.get_image("cancel_button.png")
        next_surface = common.get_image("cancel_button_pressed.png")

        self.cancel_button = ToggleTile(
            name="cancel_button",
            next_name="cancel_button",
            current_surface=surface,
            screen=self.event_handler.screen,
            size_percent=client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            tile_addition_width=0,
            tile_addition_height=0,
            next_surface=next_surface,
            shrink_percent=1,
        )

        self.set_cancel_button_size()
        self.tiles_group.add(self.cancel_button)

    def set_cancel_button_size(self):
        if not self.cancel_button:
            return

        self.cancel_button.resize()
        self.cancel_button.rect.bottom = self.game_session_name_box.rect.bottom - (
            self.event_handler.screen.get_height() * 0.05
        )
        self.cancel_button.rect.left = self.game_session_name_text.rect.left

    def build_create_button_tile(self):
        surface = common.get_image("create_game.png")
        next_surface = common.get_image("create_game_pressed.png")

        self.create_button = ToggleTile(
            name="apply_button",
            next_name="apply_button",
            current_surface=surface,
            screen=self.event_handler.screen,
            size_percent=client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            tile_addition_width=0,
            tile_addition_height=0,
            next_surface=next_surface,
            shrink_percent=1,
        )

        self.set_create_button_size()
        self.tiles_group.add(self.create_button)

    def set_create_button_size(self):
        if not self.create_button:
            return

        self.create_button.resize()
        self.create_button.rect.bottom = self.cancel_button.rect.bottom
        self.create_button.rect.right = self.game_session_name_text.rect.right

    def blit(self):
        # Refresh the object on the screen so any runtime changes will be reflected
        super().blit()
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )
        self.event_handler.screen.blit(
            self.new_game_tile.image, self.new_game_tile.rect
        )
        self.event_handler.screen.blit(
            self.settings_tile.image, self.settings_tile.rect
        )
        self.event_handler.screen.blit(self.quit_tile.image, self.quit_tile.rect)

        if self.blured_tile:
            self.event_handler.screen.blit(
                self.blured_tile.image, self.blured_tile.rect
            )
            self.event_handler.screen.blit(
                self.game_session_name_box.image, self.game_session_name_box.rect
            )
            self.game_session_name_text.blit()
            self.event_handler.screen.blit(
                self.cancel_button.image, self.cancel_button.rect
            )
            self.event_handler.screen.blit(
                self.create_button.image, self.create_button.rect
            )
            self.number_players_label.blit()
            self.number_players_dropdown.blit()

            self.private_game_label.blit()
            self.event_handler.screen.blit(
                self.private_game_toggle_button.image,
                self.private_game_toggle_button.rect,
            )

    def delete(self):
        # Apparently pygame doesn't have an option to actually delete visual objects
        # instead we should just make them transparent
        self.background_image.fill(Color(0, 0, 0))
        self.join_game_tile.image.fill(Color(0, 0, 0))
        self.new_game_tile.image.fill(Color(0, 0, 0))
        self.settings_tile.image.fill(Color(0, 0, 0))
        self.quit_tile.image.fill(Color(0, 0, 0))

        self.blit()

        del self.background_image
        del self.join_game_tile
        del self.new_game_tile
        del self.settings_tile
        del self.quit_tile

        self.tiles_group.empty()

    def open_game_name_popup(self):
        self.build_blurred_background()
        self.build_game_session_name_box()
        self.build_game_name_text_box()
        self.build_number_players_label()
        self.build_number_players_dropdown_box()
        self.build_private_game_label()
        self.build_private_game_toggle()
        self.build_cancel_button_tile()
        self.build_create_button_tile()

    def close_game_name_popup(self):
        self.tiles_group.remove(self.blured_tile)
        self.tiles_group.remove(self.game_session_name_box)
        self.tiles_group.remove(self.game_session_name_text)
        self.tiles_group.remove(self.number_players_label)
        self.tiles_group.remove(self.number_players_dropdown)
        self.tiles_group.remove(self.cancel_button)
        self.tiles_group.remove(self.create_button)
        self.tiles_group.remove(self.private_game_toggle_button)
        self.blured_tile = None
        self.game_session_name_box = None
        self.game_session_name_text = None
        self.cancel_button = None
        self.create_button = None
        self.private_game_toggle_button = None
        self.number_players_label = None
        self.number_players_dropdown = None
        self.private_game_label = None
        self.is_private_game = False
        self.players_count = "4"

    def activate_tile(self, tile, event):
        if tile.name == "new_game" and event.button == client.LEFT_BUTTON_CLICK:
            self.open_game_name_popup()
        elif tile.name == "join_game" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.join_game.open()
        elif tile.name == "settings" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.settings.open()
        elif tile.name == "quit_game" and event.button == client.LEFT_BUTTON_CLICK:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif (
            tile.name == "game_name_input" and event.button == client.LEFT_BUTTON_CLICK
        ):
            if self.game_session_name_text.text == "Game-Name":
                self.game_session_name_text.new_line()
            self.game_session_name_text.mark_clicked()
            self.event_handler.wait_text_input(self.game_session_name_text)

            # so because we have a recursion in event_handler.handle_mouse_click and event_handle.wait_text_input
            # we need to check if the button that was clicked was cancel or apply if it was we don't need to set
            # the game_session_name
            self.game_session_name = self.game_session_name_text.text if self.game_session_name_text else None
        elif (
            tile.name == "toggle_button_on" and event.button == client.LEFT_BUTTON_CLICK
        ):
            self.is_private_game = True
            self.private_game_toggle_button.next_value()
        elif (
            tile.name == "toggle_button_off"
            and event.button == client.LEFT_BUTTON_CLICK
        ):
            self.is_private_game = False
            self.private_game_toggle_button.next_value()
        elif tile.name == "cancel_button" and event.button == client.LEFT_BUTTON_CLICK:
            self.cancel_button.next_value()
            self.event_handler.handle_save_button(self.cancel_button)
            self.close_game_name_popup()
        elif tile.name == "apply_button" and event.button == client.LEFT_BUTTON_CLICK:
            self.create_button.next_value()
            self.event_handler.handle_save_button(self.create_button)
            self.game_session_name = self.game_session_name_text.text
            print(f"[STARTING GAME] {self.game_session_name}")
            self.close_game_name_popup()
            self.event_handler.lobby.open()
        elif tile.name == "players_count":

            for surface in self.number_players_dropdown.dropdown_surfaces:
                self.tiles_group.add(surface)

            if tile.text != self.number_players_dropdown.first_tile.text:
                self.number_players_dropdown.mark_clicked(tile)
                self.players_count = int(self.number_players_dropdown.first_tile.text)
                return

            self.number_players_dropdown.drop_elements()

            if not self.number_players_dropdown.active:
                for surface in self.number_players_dropdown.dropdown_surfaces:
                    self.tiles_group.remove(surface)
