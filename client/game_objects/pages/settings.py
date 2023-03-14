import pygame.image
import client
from client.game_objects.tiles.toggle_tile import ToggleTile

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.text_slideshow_tile import TextSlideshowTile


class Settings(GameWindow):
    SCREEN_SIZE_CAPTIONS = [
        "1024x620",
        "1280x720",
        "1366x768",
        "1536x864",
        "1720x880",
        "fullscreen",
    ]

    def __init__(self, screen):
        super().__init__(screen)
        self.screen_size_tile = None
        self.screen_size_right_arrow = None
        self.screen_size_left_arrow = None
        self.music_toggle = None

        self.music_state_on = True
        self.current_resolution = self.SCREEN_SIZE_CAPTIONS[1]
        # TODO: implement username
        self.current_username = None

        self.build()

    def build(self):
        self.build_background()
        self.build_screen_size_tile()
        self.build_music_toggle()

    def build_screen_size_tile(self):
        surface = pygame.image.load(f"{client.IMG_PATH}blank.png").convert_alpha()
        self.screen_size_tile = TextSlideshowTile(
            "screen_size",
            surface,
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN,
            client.TILE_WIDTH_ADDITION,
            client.TILE_HEIGHT_ADDITION,
            self.current_resolution,
            self.SCREEN_SIZE_CAPTIONS,
        )

        self.screen_size_right_arrow = self.screen_size_tile.right_arrow
        self.screen_size_left_arrow = self.screen_size_tile.left_arrow

        self.screen_size_tile.rect.centerx = self.screen_rect.centerx
        self.screen_size_tile.rect.bottom = self.screen_rect.centery - 10

        self.screen_size_tile.update()

        self.tiles_group.add(self.screen_size_right_arrow)
        self.tiles_group.add(self.screen_size_left_arrow)

    def build_music_toggle(self):
        on_surface = pygame.image.load(f"{client.IMG_PATH}button_on.png")
        off_surface = pygame.image.load(f"{client.IMG_PATH}button.png")
        self.music_toggle = ToggleTile("music_toggle_on", on_surface, self.screen, client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN, 0, 0, off_surface)

        self.music_toggle.rect.centerx = self.screen_rect.centerx
        self.music_toggle.rect.top = self.screen_rect.centery + 10

        self.tiles_group.add(self.music_toggle)

    def blit(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.screen_size_tile.image, self.screen_size_tile.rect)
        self.screen.blit(
            self.screen_size_right_arrow.image,
            self.screen_size_right_arrow.rect,
        )
        self.screen.blit(
            self.screen_size_left_arrow.image,
            self.screen_size_left_arrow.rect,
        )
        self.screen.blit(
            self.screen_size_tile.current_text_surface,
            self.screen_size_tile.current_text_rect,
        )
        self.screen.blit(
            self.music_toggle.image,
            self.music_toggle.rect
        )

    def activate_tile(self, tile, event_handler):
        if tile.name == "screen_size_right_arrow":
            self.current_resolution = self.screen_size_tile.next_text()
        if tile.name == "screen_size_left_arrow":
            self.current_resolution = self.screen_size_tile.previous_text()
        if tile.name == "music_toggle_on" or tile.name == "music_toggle_off":
            self.music_toggle.next_value()
            self.music_state_on = not self.music_state_on

        return None, False
