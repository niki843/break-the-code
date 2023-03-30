import asyncio
from collections import OrderedDict

import numpy
import pygame
import client
from client.game_objects.tiles.game_session_tile import GameSessionTile
from client.game_objects.tiles.game_sessions_group import GameSessionsGroup
from client.utils import common

from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.game_objects.tiles.tile import Tile


class JoinGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.join_game_tile = None

        self.scroll_text_tile = None

        self.game_info_tile = None
        self.game_info_box = None
        self.game_sessions_loop = None

        self.game_sessions = {}
        self.game_session_tiles = OrderedDict()
        self.clicked_game_session_tile = None
        self.game_session_group = None

        self.build()

    async def call_get_game_sessions(self):
        while True:
            self.event_handler.server_communication_manager.get_current_game()
            await asyncio.sleep(5)

    def build(self):
        super().build()
        self.build_tiles_background()

        self.build_back_tile()

        # self.build_scrollable_text()

        self.build_game_info_label()
        self.build_game_info_box()

        self.build_game_sessions_group()

        self.build_join_game_button()

    def resize(self):
        super().resize()
        self.set_tiles_background_size()

        self.set_back_tile()

        # self.set_scroll_text_size()

        self.set_game_info_label_size()
        self.set_game_info_size()

        self.set_join_game_button_size()

    def build_background(self):
        surface = common.get_image("clear_bgr.png")

        self.background_image = Tile(
            "background", surface, self.event_handler.screen, 100, 0, 0
        )
        self.set_background_size()

    def build_join_game_button(self):
        surface = common.get_image("join_game.png")

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
        surface = common.get_image("game_info.png")
        self.game_info_tile = Tile(
            name="game_info",
            surface=surface,
            screen=self.event_handler.screen,
            size_percent=25,
            tile_addition_width=0,
            tile_addition_height=0,
        )

        self.set_game_info_label_size()

    def set_game_info_label_size(self):
        if not self.game_info_tile:
            return

        self.game_info_tile.resize()
        self.game_info_tile.rect.top = self.tiles_background.rect.top + (
            self.event_handler.screen.get_height() * 0.02
        )
        self.game_info_tile.rect.right = self.tiles_background.rect.right - (
            self.event_handler.screen.get_width() * 0.03
        )

    def build_game_info_box(self):
        surface = common.get_image("game_info_menu.png")
        self.game_info_box = MultilineTextTile(
            "test_text",
            surface,
            self.event_handler.screen,
            30,
            0,
            0,
            "Player1: hasaaaaan  \n Player2: peshoslepia12 \n Player3: fikret-storaro \n Player4: neadekvaten",
            6,
            0,
        )

        self.set_game_info_size()

    def set_game_info_size(self):
        if not self.game_info_box:
            return

        self.game_info_box.resize()
        self.game_info_box.rect.bottom = self.tiles_background.rect.bottom - (
            self.event_handler.screen.get_height() * 0.02
        )
        self.game_info_box.rect.centerx = self.game_info_tile.rect.centerx
        self.game_info_box.center_text()

    def build_game_sessions_group(self):
        left = self.tiles_background.rect.left + (
            self.event_handler.screen.get_width() * 0.02
        )
        top = self.tiles_background.rect.top + (
            self.event_handler.screen.get_height() * 0.03
        )
        right = self.game_info_box.rect.left - (
            self.event_handler.screen.get_width() * 0.016
        )
        bottom = self.game_info_box.rect.bottom - (
            self.event_handler.screen.get_height() * 0.03
        )

        self.game_session_group = GameSessionsGroup(
            "game_session_group",
            "game_session_not_marked",
            "game_session_marked",
            common.get_image("game_session.png"),
            self.event_handler.screen,
            50,
            50,
            -60,
            0,
            common.get_image("game_session_selected.png"),
            6,
            left,
            top,
            right,
            bottom,
        )

        self.tiles_group.add(self.game_session_group)
        self.tiles_group.add(self.game_session_group.slider)
        self.tiles_group.add(self.game_session_group.slider.slider_handle)

    def add_or_remove_game_sessions(self, game_sessions_response):
        removed_game_sessions = self.game_session_group.game_sessions_by_id.copy()
        for game_session_id, game_session in game_sessions_response.items():
            if not self.game_session_group.tile_exists(game_session_id):
                game_session = self.game_session_group.add_game_session(
                    active_players=game_session.get("connected_players"),
                    player_usernames=game_session.get("player_id_name_map").values(),
                    game_id=game_session_id,
                    game_session_name=game_session.get("room_name"),
                )
                game_session.priority = 1
                self.tiles_group.add(game_session)
                continue
            removed_game_sessions.pop(game_session_id)

        for removed_game_session_id in removed_game_sessions.keys():
            self.tiles_group.remove(self.game_session_group.game_sessions_by_id.get(removed_game_session_id))
            self.game_session_group.delete_game_session(removed_game_session_id)

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
            self.game_info_tile.image, self.game_info_tile.rect
        )

        self.event_handler.screen.blit(
            self.game_info_box.image, self.game_info_box.rect
        )
        self.game_info_box.blit()

        self.game_session_group.blit()

        # for tile in self.game_session_tiles.values():
        #     self.event_handler.screen.blit(tile.image, tile.rect)
        #     self.event_handler.screen.blit(
        #         tile.text_box.text_surface, tile.text_box.text_rect
        #     )

    def open(self):
        super().open()
        self.game_sessions_loop = client.LOOP.create_task(self.call_get_game_sessions())

    def close(self):
        if not self.game_sessions_loop.cancelled():
            self.game_sessions_loop.cancel()

    def activate_tile(self, tile, event):
        if tile.name == "back":
            self.event_handler.menu.open()
            self.close()
        if tile.name == "handle" and event.button == client.LEFT_BUTTON_CLICK:
            self.event_handler.handle_slider_clicked(self.scroll_text_tile)
        if tile.name == "scroll_tile" and event.button == client.SCROLL_UP:
            self.scroll_text_tile.scroll_up()
            self.scroll_text_tile.slider.previous_handle_position()
        if tile.name == "scroll_tile" and event.button == client.SCROLL_DOWN:
            self.scroll_text_tile.scroll_down()
            self.scroll_text_tile.slider.next_handle_position()

        if tile.name == "game_session_marked" and event.button == client.LEFT_BUTTON_CLICK:
            tile.next_value()
            self.clicked_game_session_tile = None
        elif tile.name == "game_session_not_marked" and event.button == client.LEFT_BUTTON_CLICK:
            tile.next_value()

            if self.clicked_game_session_tile:
                self.clicked_game_session_tile.next_value()
            self.clicked_game_session_tile = tile

        if tile.name in ("game_sessions_group", "game_session_marked", "game_session_not_marked") and event.button == client.SCROLL_UP:
            self.game_session_group.slider.previous_handle_position()
            self.game_session_group.scroll_up()
        if tile.name in ("game_sessions_group", "game_session_marked", "game_session_not_marked") and event.button == client.SCROLL_DOWN:
            self.game_session_group.slider.next_handle_position()
            self.game_session_group.scroll_down()

    def delete(self):
        super().delete()
        self.join_game_tile.image.fill(pygame.Color(0, 0, 0))
        self.scroll_text_tile.image.fill(pygame.Color(0, 0, 0))
        self.tiles_background.image.fill(pygame.Color(0, 0, 0))
        self.back_tile.image.fill(pygame.Color(0, 0, 0))
        self.game_info_tile.image.fill(pygame.Color(0, 0, 0))
        self.game_info_box.image.fill(pygame.Color(0, 0, 0))

        self.blit()

        del self.join_game_tile
        del self.scroll_text_tile
        del self.tiles_background
        del self.back_tile
        del self.game_info_tile
        del self.game_info_box
