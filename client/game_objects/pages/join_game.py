import asyncio

import numpy
import pygame
import client
from client.game_objects.tiles.game_session_tile import GameSessionTile
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
        self.game_session_tiles = {}
        self.clicked_game_session_tile = None

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
            5.1,
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

    def build_game_sessions(self, game_sessions):
        self.add_new_game_tiles(game_sessions.items())
        # self.remove_closed_game_tiles(game_sessions)

    def add_new_game_tiles(self, game_sessions):
        for game_session_id, game_session in game_sessions:
            if game_session_id not in self.game_session_tiles:
                self.game_session_tiles[game_session_id] = GameSessionTile(
                    "game_session_not_marked",
                    "game_session_marked",
                    common.get_image("non_selected_nickname.png"),
                    self.event_handler.screen,
                    50,
                    50,
                    -60,
                    0,
                    common.get_image("selected_nickname.png"),
                    game_session.get("connected_players"),
                    game_session.get("player_id_name_map").values(),
                    game_session_id,
                )
                self.tiles_group.add(self.game_session_tiles[game_session_id])
            elif self.game_session_tiles.get(
                game_session_id
            ).active_players != game_session.get("connected_players"):
                self.game_session_tiles.update_players(
                    game_session.get("player_id_name_map")
                )

            self.set_game_sessions_size()

    def set_game_sessions_size(self):
        if not self.game_session_tiles:
            return

        left = self.tiles_background.rect.left + (
            self.event_handler.screen.get_width() * 0.02
        )
        top = self.tiles_background.rect.top + (
            self.event_handler.screen.get_height() * 0.03
        )

        tiles = list(self.game_session_tiles.values())

        if len(tiles) > 1:
            left = tiles[-2].rect.left
            top = tiles[-2].rect.bottom + (
                self.event_handler.screen.get_height() * 0.01
            )

        tiles[-1].rect.left = left
        tiles[-1].rect.top = top
        tiles[-1].center_text()
    # TODO: Not working yet
    # def remove_closed_game_tiles(self, game_sessions):
    #     closed_game_ids = numpy.setdiff1d(list(self.game_session_tiles.keys()), list(game_sessions.keys()))
    #
    #     for game_id in closed_game_ids:
    #         tile_to_remove = self.game_session_tiles[game_id]
    #         old_tile_position_left = tile_to_remove.rect.left
    #         old_tile_position_top = tile_to_remove.rect.top
    #         key_list = sorted(self.game_session_tiles.keys())
    #         next_tile = self.game_session_tiles.get(key_list[key_list.index(game_id) + 1])
    #         del self.game_session_tiles[game_id]
    #
    #         self.rearrange_tiles(next_tile, old_tile_position_left, old_tile_position_top)
    #
    # def rearrange_tiles(self, next_tile, left, top):
    #     next_tile.rect.left = left
    #     next_tile.rect.top = top
    #     next_tile.center_text()

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

        for tile in self.game_session_tiles.values():
            self.event_handler.screen.blit(tile.image, tile.rect)
            self.event_handler.screen.blit(
                tile.text_box.text_surface, tile.text_box.text_rect
            )

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
        if tile.name == "game_session_not_marked" and event.button == client.LEFT_BUTTON_CLICK:
            tile.next_value()

            if self.clicked_game_session_tile:
                self.clicked_game_session_tile.next_value()
            self.clicked_game_session_tile = tile

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
