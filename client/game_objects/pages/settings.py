import pygame
import client
from client.game_objects import custom_exceptions
from client.game_objects.tiles.input_box_tile import InputBoxTile
from client.game_objects.tiles.slider import Slider
from client.game_objects.tiles.tile import Tile

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.toggle_tile import ToggleTile


class Settings(GameWindow):
    SCREEN_SIZE_CAPTIONS = [
        "1024x576",
        "1280x720",
        "1366x768",
        "1536x864",
        "1720x940",
        "fullscreen",
    ]

    def __init__(self, event_handler):
        super().__init__(event_handler)
        self.settings_label_tile = None

        self.resolution_label_tile = None
        self.resolution_slider = None

        self.music_label_tile = None
        self.music_slider = None
        self.music_state_on = pygame.mixer.music.get_busy()
        self.current_volume = int(pygame.mixer.music.get_volume() * 100)

        self.username_label = None
        self.username_input_box = None
        # TODO: implement username
        self.current_username = "test"

        self.apply_button = None

        self.current_resolution = None

        self.build()

    def build(self):
        super().build()
        self.build_tiles_background()

        self.build_settings_label()

        self.build_resolution_label()
        self.build_resolution_slider()

        self.build_music_label()
        self.build_music_slider()

        self.build_username_label()
        self.build_username_text_box()

        self.build_apply_button()

        self.build_back_tile()

    def resize(self):
        super().resize()
        self.set_tiles_background_size()

        self.set_settings_label_size()

        self.set_resolution_label_size()
        self.set_resolution_slider_tile_size()

        self.set_music_label_size()
        self.set_music_slider_tile_size()

        self.set_username_label_size()
        self.set_username_text_box_size()

        self.set_apply_button_size()

        self.set_back_tile()

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_settings_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}settings_top.png"
        ).convert_alpha()

        self.settings_label_tile = Tile(
            "settings_label", surface, self.event_handler.screen, 30, 0, 0
        )
        self.set_settings_label_size()

    def set_settings_label_size(self):
        if not self.settings_label_tile:
            return

        self.settings_label_tile.resize()
        self.settings_label_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.settings_label_tile.rect.top = self.event_handler.screen_rect.top + (
            self.event_handler.screen_rect.bottom * 0.03
        )

    def build_resolution_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}res_description.png"
        ).convert_alpha()

        self.resolution_label_tile = Tile(
            "resolution_label", surface, self.event_handler.screen, 21, 0, 0
        )
        self.set_resolution_label_size()

    def set_resolution_label_size(self):
        if not self.resolution_label_tile:
            return

        self.resolution_label_tile.resize()
        self.resolution_label_tile.rect.top = self.tiles_background.rect.top + (
            self.event_handler.screen.get_height() * 0.07
        )
        self.resolution_label_tile.rect.left = self.tiles_background.rect.left + (
            self.event_handler.screen.get_width() * 0.06
        )

    def build_resolution_slider(self):
        self.current_resolution = f"{self.event_handler.screen.get_width()}x{self.event_handler.screen.get_height()}"
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_res_bar.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_button.png"
        ).convert_alpha()

        max_desktop_res = pygame.display.get_desktop_sizes()[0]
        # Check if the resolution is in the list of resolutions if not set to fullscreen
        if (
            max_desktop_res[0] == self.event_handler.screen.get_width()
            and max_desktop_res[1] == self.event_handler.screen.get_height()
        ):
            self.current_resolution = "fullscreen"

        self.resolution_slider = Slider(
            name="resolution_slider",
            surface=slider_surface,
            screen=self.event_handler.screen,
            size_percent=60,
            tile_addition_width=0,
            tile_addition_height=0,
            handle_name="resolution_slider_handle",
            handle_surface=slider_handle,
            handle_size_percent=2,
            delimiters_count=6,
            handle_position=self.SCREEN_SIZE_CAPTIONS.index(self.current_resolution),
        )
        self.set_resolution_slider_tile_size()
        self.tiles_group.add(self.resolution_slider.slider_handle)

    def set_resolution_slider_tile_size(self):
        if not self.resolution_slider:
            return

        self.resolution_slider.resize()
        self.resolution_slider.rect.top = self.resolution_label_tile.rect.bottom + (
            self.event_handler.screen.get_height() * 0.04
        )
        self.resolution_slider.rect.left = self.resolution_label_tile.rect.left
        self.resolution_slider.set_slider_handle_position()

    def build_music_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}music_description.png"
        ).convert_alpha()

        self.music_label_tile = Tile(
            "music_label", surface, self.event_handler.screen, 11, 0, 0
        )
        self.set_music_label_size()

    def set_music_label_size(self):
        if not self.music_label_tile:
            return

        self.music_label_tile.resize()
        self.music_label_tile.rect.top = self.resolution_slider.rect.bottom + (
            self.event_handler.screen.get_height() * 0.05
        )
        self.music_label_tile.rect.left = self.resolution_slider.rect.left

    def build_music_slider(self):
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_music_bar.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_button.png"
        ).convert_alpha()

        self.music_slider = Slider(
            name="music_slider",
            surface=slider_surface,
            screen=self.event_handler.screen,
            size_percent=60,
            tile_addition_width=0,
            tile_addition_height=0,
            handle_name="music_slider_handle",
            handle_surface=slider_handle,
            handle_size_percent=2,
            delimiters_count=11,
            handle_position=2,
        )
        self.set_music_slider_tile_size()
        self.tiles_group.add(self.music_slider.slider_handle)

    def set_music_slider_tile_size(self):
        if not self.music_slider:
            return

        self.music_slider.resize()
        self.music_slider.rect.top = self.music_label_tile.rect.bottom + (
            self.event_handler.screen.get_height() * 0.04
        )
        self.music_slider.rect.left = self.music_label_tile.rect.left
        self.music_slider.set_slider_handle_position()

    def build_username_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}change_nickname_description.png"
        ).convert_alpha()

        self.username_label = Tile(
            "username_label", surface, self.event_handler.screen, 33, 0, 0
        )
        self.set_username_label_size()

    def set_username_label_size(self):
        if not self.username_label:
            return

        self.username_label.resize()
        self.username_label.rect.top = self.music_slider.rect.bottom + (
            self.event_handler.screen.get_height() * 0.05
        )
        self.username_label.rect.left = self.music_slider.rect.left

    def build_username_text_box(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}non_selected_nickname.png"
        ).convert_alpha()
        next_surface = pygame.image.load(
            f"{client.IMG_PATH}selected_nickname.png"
        ).convert_alpha()

        self.username_input_box = InputBoxTile(
            "name_input",
            "name_input",
            surface,
            self.event_handler.screen,
            50,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
            next_surface,
            self.current_username,
            text_size_percentage_from_screen_height=5,
        )

        self.set_username_text_box_size()
        self.tiles_group.add(self.username_input_box)

    def set_username_text_box_size(self):
        if not self.username_input_box:
            return

        self.username_input_box.resize()
        self.username_input_box.rect.top = self.username_label.rect.bottom + (
            self.event_handler.screen.get_height() * 0.03
        )
        self.username_input_box.rect.left = self.username_label.rect.left

        self.username_input_box.center()

    def build_apply_button(self):
        surface = pygame.image.load(f"{client.IMG_PATH}apply.png").convert_alpha()
        next_surface = pygame.image.load(f"{client.IMG_PATH}apply_pressed.png").convert_alpha()

        self.apply_button = ToggleTile(
            name="apply_button_on",
            next_name="apply_button_off",
            current_surface=surface,
            screen=self.event_handler.screen,
            size_percent=client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            tile_addition_width=0,
            tile_addition_height=0,
            next_surface=next_surface,
            shrink_percent=1,
        )

        self.set_apply_button_size()
        self.tiles_group.add(self.apply_button)

    def set_apply_button_size(self):
        if not self.apply_button:
            return

        self.apply_button.resize()
        self.apply_button.rect.centery = self.username_input_box.rect.centery
        self.apply_button.rect.left = self.username_input_box.rect.right + (
            self.event_handler.screen.get_width() * 0.04
        )

    def blit(self):
        super().blit()

        self.event_handler.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )

        self.event_handler.screen.blit(
            self.settings_label_tile.image, self.settings_label_tile.rect
        )

        self.event_handler.screen.blit(
            self.resolution_label_tile.image, self.resolution_label_tile.rect
        )
        self.event_handler.screen.blit(
            self.resolution_slider.image, self.resolution_slider.rect
        )

        self.event_handler.screen.blit(
            self.music_label_tile.image, self.music_label_tile.rect
        )
        self.event_handler.screen.blit(
            self.resolution_slider.slider_handle.image,
            self.resolution_slider.slider_handle.rect,
        )

        self.event_handler.screen.blit(self.music_slider.image, self.music_slider.rect)
        self.event_handler.screen.blit(
            self.music_slider.slider_handle.image, self.music_slider.slider_handle.rect
        )

        self.event_handler.screen.blit(
            self.username_label.image, self.username_label.rect
        )
        self.event_handler.screen.blit(
            self.username_input_box.image, self.username_input_box.rect
        )
        self.event_handler.screen.blit(
            self.username_input_box.text_surface, self.username_input_box.text_rect
        )

        self.event_handler.screen.blit(self.apply_button.image, self.apply_button.rect)

        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)

    def activate_tile(self, tile, event):
        if (
            tile.name == "resolution_slider_handle"
            and event.button == client.LEFT_BUTTON_CLICK
        ):
            self.event_handler.handle_slider_clicked(self.resolution_slider)

            try:
                self.current_resolution = self.SCREEN_SIZE_CAPTIONS[
                    self.resolution_slider.get_index()
                ]
            except IndexError:
                raise custom_exceptions.ScreenResolutionIndexError()

            self.change_screen_resolution_and_rebuild(self.current_resolution)
        if (
            tile.name == "music_slider_handle"
            and event.button == client.LEFT_BUTTON_CLICK
        ):
            self.event_handler.handle_slider_clicked(self.music_slider)

            try:
                self.current_volume = int(self.music_slider.get_index() * 10)
            except IndexError:
                raise custom_exceptions.VolumeIndexError()

            if self.current_volume > 0:
                pygame.mixer.music.set_volume(self.current_volume / 100)
                if not self.music_state_on:
                    self.music_state_on = True
                    pygame.mixer.music.play(-1)

            if self.current_volume <= 0:
                self.music_state_on = False
                pygame.mixer.music.stop()
        if (
            tile.name == "apply_button_on" or tile.name == "apply_button_off"
        ) and event.button == client.LEFT_BUTTON_CLICK:
            self.apply_button.next_value()
            # Save the username if only it's not empty
            if len(self.username_input_box.text) > 0:
                self.current_username = self.username_input_box.text
            self.event_handler.handle_save_button(self.apply_button)
        if tile.name == "back" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.change_window(self.event_handler.menu)
            self.username_input_box.text = self.current_username
            self.username_input_box.resize_text()
            self.username_input_box.center()
        if tile.name == "name_input" and event.button == client.LEFT_BUTTON_CLICK:
            self.username_input_box.mark_clicked()
            return self.event_handler.wait_text_input(self.username_input_box)
        return None, False

    def change_screen_resolution_and_rebuild(self, resolution: str):
        if resolution == "fullscreen":
            self.event_handler.change_screen(
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            )
        else:
            resolution_params = [int(res) for res in resolution.split("x")]
            self.event_handler.change_screen(
                pygame.display.set_mode(
                    (resolution_params[0], resolution_params[1]),
                    pygame.HWSURFACE | pygame.DOUBLEBUF,
                )
            )

    def delete(self):
        # Apparently pygame doesn't have an option to actually delete visual objects
        # instead we should just make them transparent
        self.background_image.image.fill(pygame.Color(0, 0, 0))
        self.screen_size_tile.image.fill(pygame.Color(0, 0, 0))
        self.screen_size_right_arrow.image.fill(pygame.Color(0, 0, 0))
        self.screen_size_left_arrow.image.fill(pygame.Color(0, 0, 0))
        self.screen_size_tile.current_text_surface.fill(pygame.Color(0, 0, 0))
        self.music_toggle.image.fill(pygame.Color(0, 0, 0))

        self.blit()

        del self.background_image
        del self.screen_size_right_arrow
        del self.screen_size_left_arrow
        del self.screen_size_tile.current_text_surface
        del self.music_toggle

        self.tiles_group.empty()
