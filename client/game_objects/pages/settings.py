import pygame
import client
from client.game_objects import custom_exceptions
from client.game_objects.tiles.input_box_tile import InputBoxTile
from client.game_objects.tiles.slider import Slider
from client.game_objects.tiles.tile import Tile
from client.game_objects.tiles.toggle_tile import ToggleTile

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.text_slideshow_tile import TextSlideshowTile


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
        self.screen_size_tile = None
        self.screen_size_right_arrow = None
        self.screen_size_left_arrow = None
        self.music_toggle = None
        self.name_input_box = None
        self.slider_resolution = None
        self.back_tile = None
        self.tiles_background = None
        self.settings_label_tile = None
        self.resolution_label_tile = None

        self.music_state_on = pygame.mixer.music.get_busy()
        self.current_resolution = None
        # TODO: implement username
        self.current_username = "test"
        self.temp_username = None

        self.build()

    def build(self):
        self.build_background()
        self.build_tiles_background()
        self.build_settings_label()
        self.build_resolution_label()
        self.build_music_toggle()
        self.build_username_text_box()
        self.build_resolution_slider()
        self.build_back_tile()

    def resize(self):
        self.set_background_size()
        self.set_tiles_background_size()
        self.set_settings_label_size()
        self.set_resolution_label_size()
        self.set_music_toggle_size()
        self.set_username_text_box_size()
        self.set_resolution_slider_tile_size()
        self.set_back_tile()

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_tiles_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}menu_field.png").convert_alpha()

        self.tiles_background = Tile(
            "tiles_background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_tiles_background_size()

    def set_tiles_background_size(self):
        if not self.tiles_background:
            return
        self.tiles_background.resize()
        self.tiles_background.rect.centerx = self.event_handler.screen_rect.centerx
        self.tiles_background.rect.centery = self.event_handler.screen_rect.centery

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
            "resolution_label", surface, self.event_handler.screen, 30, 0, 0
        )
        self.set_resolution_label_size()

    def set_resolution_label_size(self):
        if not self.resolution_label_tile:
            return

        self.resolution_label_tile.resize()
        self.resolution_label_tile.rect.top = self.tiles_background.rect.top + (
            self.event_handler.screen_rect.bottom * 0.22
        )
        self.resolution_label_tile.rect.left = self.tiles_background.rect.left + (
            self.event_handler.screen_rect.right * 0.16
        )

    def build_resolution_slider(self):
        self.current_resolution = f"{self.event_handler.screen.get_width()}x{self.event_handler.screen.get_height()}"
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_res_bar.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_handle.png"
        ).convert_alpha()

        max_desktop_res = pygame.display.get_desktop_sizes()[0]
        # Check if the resolution is in the list of resolutions if not set to fullscreen
        if (
            max_desktop_res[0] == self.event_handler.screen.get_width()
            and max_desktop_res[1] == self.event_handler.screen.get_height()
        ):
            self.current_resolution = "fullscreen"

        self.slider_resolution = Slider(
            name="slider",
            surface=slider_surface,
            screen=self.event_handler.screen,
            size_percent=60,
            tile_addition_width=0,
            tile_addition_height=0,
            handle_name="slider_handle",
            handle_surface=slider_handle,
            handle_size_percent=2,
            delimiters_count=6,
            handle_position=self.SCREEN_SIZE_CAPTIONS.index(self.current_resolution),
        )
        self.set_resolution_slider_tile_size()
        self.tiles_group.add(self.slider_resolution.slider_handle)

    def set_resolution_slider_tile_size(self):
        if not self.slider_resolution:
            return

        self.slider_resolution.resize()
        self.slider_resolution.rect.top = self.resolution_label_tile.rect.top + (
            self.event_handler.screen_rect.bottom * 0.11
        )
        self.slider_resolution.rect.left = self.resolution_label_tile.rect.left
        self.slider_resolution.set_slider_handle_position()

    def build_screen_resolution_slide(self):
        pass

    def build_music_toggle(self):
        on_surface = pygame.image.load(
            f"{client.IMG_PATH}button_on2.png"
        ).convert_alpha()
        off_surface = pygame.image.load(f"{client.IMG_PATH}button2.png").convert_alpha()

        # Use the appropriate image for the music when screen size is changed and the settings window is being re-build
        current_surface = on_surface if self.music_state_on else off_surface
        next_surface = off_surface if self.music_state_on else on_surface

        self.music_toggle = ToggleTile(
            "music_toggle_on" if self.music_state_on else "music_toggle_off",
            "music_toggle_off" if self.music_state_on else "music_toggle_on",
            current_surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            0,
            0,
            next_surface,
        )

        self.set_music_toggle_size()
        self.tiles_group.add(self.music_toggle)

    def set_music_toggle_size(self):
        if not self.music_toggle:
            return

        self.music_toggle.resize()
        self.music_toggle.rect.centerx = self.event_handler.screen_rect.centerx
        self.music_toggle.rect.top = self.event_handler.screen_rect.centery + 15

    def build_username_text_box(self):
        surface = pygame.image.load(f"{client.IMG_PATH}blank.png").convert_alpha()
        next_surface = pygame.image.load(
            f"{client.IMG_PATH}blank_highlight.png"
        ).convert_alpha()
        self.name_input_box = InputBoxTile(
            "name_input",
            "name_input",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
            next_surface,
            self.temp_username if self.temp_username else self.current_username,
            text_size_percentage_from_screen_height=10,
        )

        self.set_username_text_box_size()
        self.tiles_group.add(self.name_input_box)

    def set_username_text_box_size(self):
        if not self.name_input_box:
            return

        self.name_input_box.resize()
        self.name_input_box.rect.centerx = self.event_handler.screen_rect.centerx
        self.name_input_box.rect.top = self.music_toggle.rect.bottom + 15

        self.name_input_box.text_rect.centerx = self.name_input_box.rect.centerx
        self.name_input_box.text_rect.centery = self.name_input_box.rect.centery

    def build_back_tile(self):
        back_surface = pygame.image.load(f"{client.IMG_PATH}back.png")
        self.back_tile = Tile(
            "back",
            back_surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            0,
            0,
        )

        self.set_back_tile()
        self.tiles_group.add(self.back_tile)

    def set_back_tile(self):
        if not self.back_tile:
            return

        self.back_tile.resize()
        self.back_tile.rect.left = self.event_handler.screen_rect.left + 40
        self.back_tile.rect.top = self.event_handler.screen_rect.top + 20

    def blit(self):
        self.event_handler.screen.blit(
            self.background_image.image, self.background_image.rect
        )
        self.event_handler.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )
        self.event_handler.screen.blit(
            self.settings_label_tile.image, self.settings_label_tile.rect
        )
        self.event_handler.screen.blit(
            self.resolution_label_tile.image, self.resolution_label_tile.rect
        )
        self.event_handler.screen.blit(self.music_toggle.image, self.music_toggle.rect)
        self.event_handler.screen.blit(
            self.name_input_box.image, self.name_input_box.rect
        )
        self.event_handler.screen.blit(
            self.name_input_box.text_surface, self.name_input_box.text_rect
        )
        self.event_handler.screen.blit(self.slider_resolution.image, self.slider_resolution.rect)
        self.event_handler.screen.blit(
            self.slider_resolution.slider_handle.image, self.slider_resolution.slider_handle.rect
        )
        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)

    def activate_tile(self, tile):
        if tile.name == "music_toggle_on" or tile.name == "music_toggle_off":
            self.music_toggle.next_value()
            self.music_state_on = not self.music_state_on

            pygame.mixer.music.stop()
            if self.music_state_on:
                pygame.mixer.music.play(-1)
        if tile.name == "name_input":
            self.name_input_box.mark_clicked()
            return self.event_handler.wait_text_input(self.name_input_box)
        if tile.name == "slider_handle":
            self.event_handler.handle_slider_clicked(self.slider_resolution)

            try:
                self.current_resolution = self.SCREEN_SIZE_CAPTIONS[self.slider_resolution.get_index()]
            except IndexError:
                raise custom_exceptions.ScreenResolutionSliderException()

            self.change_screen_resolution_and_rebuild(self.current_resolution)
        if tile.name == "back":
            self.event_handler.change_window(self.event_handler.menu)

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

        self.temp_username = self.name_input_box.text

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
