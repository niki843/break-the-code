import client

from client.game_objects.tiles.tile import Tile
from client.utils import common


class PlayedCardsPopupGroup:
    def __init__(self, group_name, tiles_group):
        self.group_name = group_name
        self.played_cards_and_player_responses = {}

        self.played_cards_button = None

        self.background = None

        self.tiles_group = tiles_group

        self.is_open = False

        self.build()

    def add_played_card(self, played_card_tile: Tile, player_responses: dict):
        self.played_cards_and_player_responses.update({played_card_tile: player_responses})

    def build(self):
        self.build_background()
        self.build_played_cards_button()

    def resize(self):
        self.set_background_size()
        self.set_played_cards_button_size()

    def clicked(self):
        self.close() if self.is_open else self.open()

    def open(self):

        self.is_open = True

        self.resize()

    def close(self):
        self.is_open = False

        self.resize()

    def build_background(self):
        self.background = common.load_tile("played_cards_background", common.get_image("guess_card_bgr_cropped.png"), 30.3, client.state_manager.screen)

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
        self.played_cards_button = common.load_rotated_right_tile("played_cards_arrow", "played_cards_arrow.png", 3.5, client.state_manager.screen)

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

    def blit(self):
        client.state_manager.screen.blit(self.played_cards_button.image, self.played_cards_button.rect)

        if self.is_open:
            client.state_manager.screen.blit(self.background.image, self.background.rect)
