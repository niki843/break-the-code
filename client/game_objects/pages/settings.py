import pygame
import client
from client.game_objects.tiles.input_box_tile import InputBoxTile
from client.game_objects.tiles.slider import Slider
from client.game_objects.tiles.tile import Tile
from client.game_objects.tiles.toggle_tile import ToggleTile

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.text_slideshow_tile import TextSlideshowTile


class Settings(GameWindow):
    SCREEN_SIZE_CAPTIONS = [
        "1024x620",
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
        self.slider = None
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
        self.build_buttons_background()
        self.build_settings_label()
        self.build_resolution_label()
        self.build_screen_size_tile()
        self.build_music_toggle()
        self.build_username_text_box()
        self.build_slider()
        self.build_back_tile()

    def build_background(self):
        self.background_image = pygame.image.load(
            f"{client.IMG_PATH}clear_bgr.png"
        ).convert_alpha()

        self.background_image = pygame.transform.scale(
            self.background_image,
            (
                self.event_handler.screen.get_width(),
                self.event_handler.screen.get_height(),
            ),
        )
        self.background_rect = self.background_image.get_rect()

    def build_buttons_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}menu_field.png").convert_alpha()

        self.tiles_background = Tile(
            "tiles_background", surface, self.event_handler.screen, 100, 0, 0
        )

        self.tiles_background.rect.centerx = self.event_handler.screen_rect.centerx
        self.tiles_background.rect.centery = self.event_handler.screen_rect.centery

    def build_settings_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}settings_top.png"
        ).convert_alpha()

        self.settings_label_tile = Tile(
            "settings_label", surface, self.event_handler.screen, 30, 0, 0
        )

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

        self.resolution_label_tile.rect.top = self.tiles_background.rect.top + (
            self.event_handler.screen_rect.bottom * 0.22
        )
        self.resolution_label_tile.rect.left = self.tiles_background.rect.left + (
            self.event_handler.screen_rect.right * 0.16
        )

    def build_slider(self):
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_res_bar.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_handle.png"
        ).convert_alpha()
        self.slider = Slider(
            "slider",
            slider_surface,
            self.event_handler.screen,
            60,
            0,
            0,
            "slider_handle",
            slider_handle,
            2,
            8,
        )

        self.slider.rect.top = self.resolution_label_tile.rect.top + (
            self.event_handler.screen_rect.bottom * 0.11
        )
        self.slider.rect.left = self.resolution_label_tile.rect.left
        self.slider.slider_handle.rect.centerx = self.slider.rect.centerx
        self.slider.slider_handle.rect.centery = self.slider.rect.centery

        self.tiles_group.add(self.slider.slider_handle)

    def build_screen_size_tile(self):
        surface = pygame.image.load(f"{client.IMG_PATH}blank.png").convert_alpha()
        self.current_resolution = f"{self.event_handler.screen.get_width()}x{self.event_handler.screen.get_height()}"

        max_desktop_res = pygame.display.get_desktop_sizes()[0]

        # Check if the resolution is in the list of resolutions if not set to fullscreen
        if (
            max_desktop_res[0] == self.event_handler.screen.get_width()
            and max_desktop_res[1] == self.event_handler.screen.get_height()
        ):
            self.current_resolution = "fullscreen"

        self.screen_size_tile = TextSlideshowTile(
            "screen_size",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
            self.current_resolution,
            self.SCREEN_SIZE_CAPTIONS,
        )

        self.screen_size_right_arrow = self.screen_size_tile.right_arrow
        self.screen_size_left_arrow = self.screen_size_tile.left_arrow

        self.screen_size_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.screen_size_tile.rect.bottom = self.event_handler.screen_rect.centery - 15

        self.screen_size_tile.update()

        self.tiles_group.add(self.screen_size_right_arrow)
        self.tiles_group.add(self.screen_size_left_arrow)

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

        self.music_toggle.rect.centerx = self.event_handler.screen_rect.centerx
        self.music_toggle.rect.top = self.event_handler.screen_rect.centery + 15

        self.tiles_group.add(self.music_toggle)

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
            50,
        )

        self.name_input_box.rect.centerx = self.event_handler.screen_rect.centerx
        self.name_input_box.rect.top = self.music_toggle.rect.bottom + 15

        self.name_input_box.text_rect.centerx = self.name_input_box.rect.centerx
        self.name_input_box.text_rect.centery = self.name_input_box.rect.centery

        self.tiles_group.add(self.name_input_box)

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

        self.back_tile.rect.left = self.event_handler.screen_rect.left + 40
        self.back_tile.rect.top = self.event_handler.screen_rect.top + 20

        self.tiles_group.add(self.back_tile)

    def blit(self):
        self.event_handler.screen.blit(self.background_image, self.background_rect)
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
            self.screen_size_tile.image, self.screen_size_tile.rect
        )
        self.event_handler.screen.blit(
            self.screen_size_right_arrow.image,
            self.screen_size_right_arrow.rect,
        )
        self.event_handler.screen.blit(
            self.screen_size_left_arrow.image,
            self.screen_size_left_arrow.rect,
        )
        self.event_handler.screen.blit(
            self.screen_size_tile.current_text_surface,
            self.screen_size_tile.current_text_rect,
        )
        self.event_handler.screen.blit(self.music_toggle.image, self.music_toggle.rect)
        self.event_handler.screen.blit(
            self.name_input_box.image, self.name_input_box.rect
        )
        self.event_handler.screen.blit(
            self.name_input_box.text_surface, self.name_input_box.text_rect
        )
        self.event_handler.screen.blit(self.slider.image, self.slider.rect)
        self.event_handler.screen.blit(
            self.slider.slider_handle.image, self.slider.slider_handle.rect
        )
        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)

    def activate_tile(self, tile):
        if tile.name == "screen_size_right_arrow":
            self.current_resolution = self.screen_size_tile.next_text()
            self.change_screen_resolution_and_rebuild(self.current_resolution)
        if tile.name == "screen_size_left_arrow":
            self.current_resolution = self.screen_size_tile.previous_text()
            self.change_screen_resolution_and_rebuild(self.current_resolution)
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
            self.event_handler.handle_slider_clicked(self.slider)
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
        self.background_image.fill(pygame.Color(0, 0, 0))
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
