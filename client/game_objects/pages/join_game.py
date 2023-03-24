import pygame
import client

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.game_objects.tiles.scroll_text_tile import ScrollTextTile
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None

        self.scroll_text_tile = None

        self.game_info_tile = None

        self.text_box = None

        self.build()

    def build(self):
        super().build()
        self.build_tiles_background()

        self.build_back_tile()

        # self.build_scrollable_text()

        self.build_game_info_label()

        self.build_join_game_button()

        self.build_text_box()

    def resize(self):
        super().resize()
        self.set_tiles_background_size()

        self.set_back_tile()

        # self.set_scroll_text_size()

        self.set_game_info_size()

        self.set_join_game_button_size()

        self.set_text_box_size()

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

    # def build_scrollable_text(self):
    #     surface = pygame.image.load(
    #         f"{client.IMG_PATH}menu_field_cropped.png"
    #     ).convert_alpha()
    #     slider_surface = pygame.image.load(
    #         f"{client.IMG_PATH}slider_vertical.png"
    #     ).convert_alpha()
    #     slider_handle = pygame.image.load(
    #         f"{client.IMG_PATH}slider_button.png"
    #     ).convert_alpha()
    #
    #     self.scroll_text_tile = ScrollTextTile(
    #         name="scroll_tile",
    #         slider_name="slider",
    #         handle_name="handle",
    #         main_background_surface=surface,
    #         slider_surface=slider_surface,
    #         handle_surface=slider_handle,
    #         screen=self.event_handler.screen,
    #         size_percent=49,
    #         tile_addition_width=-(self.event_handler.screen.get_width() * 0.2),
    #         tile_addition_height=self.event_handler.screen.get_height() * 0.2,
    #         text_to_display="Player1: haaaaasaaaan 12344543643523232343241224 \n 1 \n Player2: peshoslep12 Player3: gosho, idawdadvdfbfdgbd , fsdgbdfbdfb qwfvfdbdtfbsa sawdsabdf awfvfdbdfbndrt efvdfbdfbernb ewegbreber vrsegbrebernbb niki",
    #         text_size_percentage=6,
    #     )
    #
    #     self.set_scroll_text_size()
    #
    # def set_scroll_text_size(self):
    #     if not self.scroll_text_tile:
    #         return
    #
    #     self.scroll_text_tile.resize()
    #     self.scroll_text_tile.rect.right = self.tiles_background.rect.right - (
    #         self.event_handler.screen.get_width() * 0.01
    #     )
    #     self.scroll_text_tile.rect.centery = self.tiles_background.rect.centery - (
    #         self.event_handler.screen.get_height() * 0.001
    #     )
    #
    #     self.scroll_text_tile.center_elements()
    #
    #     self.tiles_group.add(self.scroll_text_tile.slider.slider_handle)
    #     self.tiles_group.add(self.scroll_text_tile)

    def build_game_info_label(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}game_info.png"
        ).convert_alpha()
        self.game_info_tile = Tile(
            name="game_info",
            surface=surface,
            screen=self.event_handler.screen,
            size_percent=25,
            tile_addition_width=0,
            tile_addition_height=0
        )

        self.set_game_info_size()

    def set_game_info_size(self):
        if not self.game_info_tile:
            return

        self.game_info_tile.resize()
        self.game_info_tile.rect.top = self.tiles_background.rect.top + (
            self.event_handler.screen.get_height() * 0.02
        )
        self.game_info_tile.rect.right = self.tiles_background.rect.right - (
            self.event_handler.screen.get_width() * 0.03
        )

    def build_text_box(self):
        surface = pygame.image.load(
            f"{client.IMG_PATH}menu_field_cropped.png"
        ).convert_alpha()
        self.text_box = MultilineTextTile(
            "test_text",
            surface,
            self.event_handler.screen,
            78,
            -660,
            -100,
            """
            Player1: hasaaaaan 
            Player2: peshoslepia12 
            Player3: fikret-storaro
            Player4: neadekvaten""",
            5.1,
            1
        )

        self.set_text_box_size()

    def set_text_box_size(self):
        if not self.text_box:
            return

        self.text_box.resize()
        self.text_box.rect.top = self.game_info_tile.rect.bottom + (
            self.event_handler.screen.get_height() * 0.005
        )
        self.text_box.rect.centerx = self.game_info_tile.rect.centerx
        self.text_box.center_text()

    def blit(self):
        super().blit()
        self.event_handler.screen.blit(
            self.tiles_background.image, self.tiles_background.rect
        )

        self.event_handler.screen.blit(self.back_tile.image, self.back_tile.rect)
        self.event_handler.screen.blit(
            self.join_game_tile.image, self.join_game_tile.rect
        )
        # self.event_handler.screen.blit(
        #     self.scroll_text_tile.image, self.scroll_text_tile.rect
        # )
        # self.scroll_text_tile.blit()

        self.event_handler.screen.blit(
            self.game_info_tile.image,
            self.game_info_tile.rect
        )

        self.event_handler.screen.blit(
            self.text_box.image, self.text_box.rect
        )
        self.text_box.blit()

    def activate_tile(self, tile, event):
        if tile.name == "back":
            self.event_handler.change_window(self.event_handler.menu)
        if tile.name == "handle" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.handle_slider_clicked(self.scroll_text_tile)
        if tile.name == "scroll_tile" and event.button == client.SCROLL_UP:
            self.scroll_text_tile.scroll_up()
            self.scroll_text_tile.slider.previous_handle_position()
        if tile.name == "scroll_tile" and event.button == client.SCROLL_DOWN:
            self.scroll_text_tile.scroll_down()
            self.scroll_text_tile.slider.next_handle_position()

        return None, False
