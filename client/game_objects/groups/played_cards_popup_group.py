import client
from client.game_objects.tiles.height_resizable_multiline_text_tile import HeightResizableMultilineTextTile
from client.game_objects.tiles.slider import Slider

from client.game_objects.tiles.tile import Tile
from client.utils import common


class PlayedCardsPopupGroup:
    def __init__(self, group_name, tiles_group):
        self.group_name = group_name
        self.played_cards_and_player_responses = []

        self.played_cards_button = None

        self.scroll = None

        self.background = None

        self.tiles_group = tiles_group

        self.is_open = False

        self.build()

    def add_played_card(self, played_card_tile: Tile, player_responses: dict):
        player_response_tiles = []
        for name, response in player_responses.items():
            player_response_tiles.append(
                HeightResizableMultilineTextTile(
                    name="player_response",
                    screen=client.state_manager.screen,
                    width_percent=35,
                    text_to_display=f"{name}: {response}",
                    text_size_percent=5,
                    start_line=0
                )
            )

        self.played_cards_and_player_responses.append(
            (played_card_tile, player_response_tiles)
        )

        played_card_tile.size_percent = 23
        played_card_tile.resize()

        self.set_player_responses_size(played_card_tile, player_response_tiles)

    def set_played_cards_size(self):
        top = self.background.rect.top + (self.background.image.get_height() * 0.01)
        for card, player_responses in self.played_cards_and_player_responses:
            card.resize()
            card.rect.centerx = self.background.rect.centerx
            card.rect.top = top

            top = self.set_player_responses_size(card, player_responses)

    def set_player_responses_size(self, card_tile, response_tiles):
        top = card_tile.rect.bottom + (
            self.background.image.get_height() * 0.02
        )
        for response_tile in response_tiles:
            response_tile.resize()
            response_tile.rect.left = self.background.rect.left + (
                self.background.image.get_width() * 0.05
            )
            response_tile.rect.top = top
            response_tile.center_text()

            top = response_tile.rect.bottom + (
                self.background.image.get_height() * 0.02
            )
        return top

    def build(self):
        self.build_background()
        self.build_played_cards_button()
        self.build_scroll()

    def resize(self):
        self.set_background_size()
        self.set_played_cards_button_size()
        self.set_played_cards_size()
        self.set_scroll_size()

    def clicked(self):
        self.close() if self.is_open else self.open()

    def open(self):

        self.is_open = True

        self.resize()

    def close(self):
        self.is_open = False

        self.resize()

    def build_background(self):
        self.background = common.load_tile(
            "played_cards_background",
            common.get_image("guess_card_bgr_cropped.png"),
            30.3,
            client.state_manager.screen,
        )

        self.set_background_size()

    def set_background_size(self):
        if not self.background:
            return

        self.background.resize()
        self.background.rect.top = client.state_manager.screen_rect.top

        if self.is_open:
            self.background.rect.right = client.state_manager.screen_rect.right
        else:
            self.background.rect.left = client.state_manager.screen_rect.right

    def build_played_cards_button(self):
        self.played_cards_button = common.load_rotated_right_tile(
            "played_cards_arrow",
            "played_cards_arrow.png",
            3.5,
            client.state_manager.screen,
        )

        self.tiles_group.add(self.played_cards_button)
        self.set_played_cards_button_size()

    def set_played_cards_button_size(self):
        if not self.played_cards_button:
            return

        self.played_cards_button.resize()
        self.played_cards_button.rect.top = client.state_manager.screen_rect.top + (
            client.state_manager.screen.get_width() * 0.01
        )
        self.played_cards_button.rect.right = self.background.rect.left

    def build_scroll(self):
        self.scroll = Slider(
            name="game_sessions_slider",
            surface=common.get_image("scroll_bar.png"),
            screen=client.state_manager.screen,
            size_percent=1,
            handle_name="game_session_slider_handle",
            handle_surface=common.get_image("slider_button.png"),
            handle_size_percent=1.1,
            delimiters_count=3,
            handle_position=0,
            horizontal=False,
            tile_addition_width_percent=0.2,
            tile_addition_height_percent=26
        )

        self.set_scroll_size()

    def set_scroll_size(self):
        if not self.scroll:
            return

        self.scroll.resize()
        self.scroll.rect.right = self.background.rect.right
        self.scroll.rect.top = self.background.rect.top
        self.scroll.update_slider_handle_by_position()

    def blit(self):
        client.state_manager.screen.blit(
            self.played_cards_button.image, self.played_cards_button.rect
        )

        if self.is_open:
            client.state_manager.screen.blit(
                self.background.image, self.background.rect
            )
            for card, player_response_tiles in self.played_cards_and_player_responses:
                client.state_manager.screen.blit(card.image, card.rect)
                for player_response_tile in player_response_tiles:
                    player_response_tile.blit()

            self.scroll.blit()
