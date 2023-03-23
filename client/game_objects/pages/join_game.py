import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.scroll_text_tile import ScrollTextTile
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None

        self.scroll_text_tile = None

        self.build()

    def build(self):
        super().build()
        self.build_tiles_background()

        self.build_back_tile()

        self.build_scrollable_text()

        self.build_join_game_button()

    def resize(self):
        super().resize()
        self.set_tiles_background_size()

        self.set_back_tile()

        self.set_scroll_text_size()

        self.set_join_game_button_size()

    def build_background(self):
        surface = pygame.image.load(f"{client.IMG_PATH}clear_bgr.png").convert_alpha()

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_join_game_button(self):
        surface = pygame.image.load(f"{client.IMG_PATH}join_game.png").convert_alpha()

        self.join_game_tile = Tile(
            "join_game_button",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            10,
            0,
        )

        self.set_join_game_button_size()

    def set_join_game_button_size(self):
        if not self.join_game_tile:
            return

        self.join_game_tile.resize()
        self.join_game_tile.rect.right = self.event_handler.screen_rect.right - (
            self.event_handler.screen.get_width() * 0.03
        )
        self.join_game_tile.rect.bottom = self.event_handler.screen_rect.bottom - (
            self.event_handler.screen.get_height() * 0.03
        )
        self.tiles_group.add(self.join_game_tile)

    def build_scrollable_text(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}menu_field_cropped.png"
        ).convert_alpha()
        slider_surface = pygame.image.load(
            f"{client.IMG_PATH}slider_vertical.png"
        ).convert_alpha()
        slider_handle = pygame.image.load(
            f"{client.IMG_PATH}slider_button.png"
        ).convert_alpha()

        self.scroll_text_tile = ScrollTextTile(
            name="scroll_tile",
            slider_name="slider",
            handle_name="handle",
            left_arrow_name="left_arrow",
            right_arrow_name="right_arrow",
            main_background_surface=surface,
            slider_surface=slider_surface,
            handle_surface=slider_handle,
            screen=self.event_handler.screen,
            size_percent=49,
            arrow_size_percent=2,
            slider_size_percent=4,
            slider_handle_size_percent=4,
            tile_addition_width=-(self.event_handler.screen.get_width() * 0.2),
            tile_addition_height=self.event_handler.screen.get_height() * 0.2,
            text_items=[
                "some fucking shit",
                "test2",
                "test3",
                "test4",
                "test5",
                "test6",
                "test 7",
                "test 8",
                "test 9",
                "test 10",
                "test 11",
                "test 12",
            ],
            max_elements_to_display=6,
            text_size_percentage=10,
        )

        self.set_scroll_text_size()

    def set_scroll_text_size(self):
        if not self.scroll_text_tile:
            return

        self.scroll_text_tile.resize()
        self.scroll_text_tile.rect.right = self.tiles_background.rect.right - (
            self.event_handler.screen.get_width() * 0.134
        )
        self.scroll_text_tile.rect.centery = self.tiles_background.rect.centery - 3

        self.scroll_text_tile.update()

        self.tiles_group.add(self.scroll_text_tile.right_arrow)
        self.tiles_group.add(self.scroll_text_tile.left_arrow)
        self.tiles_group.add(self.scroll_text_tile.slider.slider_handle)
        self.tiles_group.add(self.scroll_text_tile)

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )

        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )
        self.event_handler.screen.blit(
            self.scroll_text_tile.image, self.scroll_text_tile.rect
        )
        self.scroll_text_tile.blit_text()

    def activate_tile(self, tile, event):
        if tile.name == "back":
            self.event_handler.change_window(self.event_handler.menu)
        if tile.name == "right_arrow" and event.button == client.LEFT_BUTTON_CLICK:
            self.scroll_text_tile.next_text()
            self.scroll_text_tile.slider.next_handle_position()
        if tile.name == "left_arrow" and event.button == client.LEFT_BUTTON_CLICK:
            self.scroll_text_tile.previous_text()
            self.scroll_text_tile.slider.previous_handle_position()
        if tile.name == "handle" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.handle_slider_clicked(self.scroll_text_tile)
        if tile.name == "scroll_tile" and event.button == client.SCROLL_UP:
            self.scroll_text_tile.previous_text()
            self.scroll_text_tile.slider.previous_handle_position()
        if tile.name == "scroll_tile" and event.button == client.SCROLL_DOWN:
            self.scroll_text_tile.next_text()
            self.scroll_text_tile.slider.next_handle_position()

        return None, False
