from types import SimpleNamespace

import client
from client.game_objects.cards.card_reader import CardReader
from client.game_objects.custom_exceptions.no_such_card_exception import NoSuchCardException
from client.game_objects.groups.condition_cards_group import ConditionCardsGroup
from client.game_objects.groups.player_number_tiles_group import PlayerNumberTilesGroup
from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile
from client.utils import common
from client.utils.enums import Colors


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.non_played_condition_cards = {}
        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        self.number_cards = []

        self.host_id = None
        self.host_username = None

        self.condition_cards_group = None
        self.player_number_tiles_group = None

        self.shown_cards = []

        self.build()

    def build(self):
        self.build_new_game_background()

    def resize(self):
        super().resize()

        self.set_condition_cards_size()

        self.set_player_number_group_size()

    def build_draw_pile(self, condition_cards):
        self.condition_cards_group = ConditionCardsGroup(
            "condition_cards_group",
            "condition_card",
            self.event_handler.screen,
            condition_cards,
        )

        self.set_condition_cards_size()

    def set_condition_cards_size(self):
        if not self.condition_cards_group:
            return

        self.condition_cards_group.resize()

    def load_number_cards(self, number_cards):
        for card in number_cards:
            self.number_cards.append(
                Tile(
                    "number_card",
                    common.get_image(f"{card.get('number')}_{Colors(card.get('color'))}.png"),
                    self.event_handler.screen,
                    5,
                    0,
                    0,
                )
            )
        self.build_player_number_group()

    def build_player_number_group(self):
        self.player_number_tiles_group = PlayerNumberTilesGroup(
            "player_number_group",
            "number_card",
            self.event_handler.screen,
            self.event_handler.screen_rect,
            self.player_info_group.connected_players,
            self.number_cards,
        )

        self.set_player_number_group_size()

    def set_player_number_group_size(self):
        if not self.player_number_tiles_group:
            return

        self.player_number_tiles_group.resize()
        self.player_number_tiles_group.center()

    def open(self, **kwargs):
        super().open()
        self.event_handler.server_communication_manager.send_start_game_message()
        cr = CardReader()

        self.player_info_group = kwargs.get("player_info_group")
        self.host_id = kwargs.get("host_id")
        self.host_username = kwargs.get("host_username")

        for card in cr.cards:
            self.non_played_condition_cards[card.id] = card

    def load_condition_cards(self, card_ids):
        if self.current_drawn_condition_cards or self.played_condition_cards:
            return

        for card_id in card_ids:
            if card_id in self.current_drawn_condition_cards:
                continue
            card = self.non_played_condition_cards.pop(int(card_id))
            self.current_drawn_condition_cards[card_id] = card

        self.build_draw_pile(self.current_drawn_condition_cards.values())
        self.tiles_group.add(self.condition_cards_group.condition_card_tiles)

    def replace_card_and_give_result(self, card_id, next_card_id, card_description):
        self.remove_played_card(card_id)
        self.draw_condition_card(next_card_id)

        new_card = Tile(
            f"condition_card-{next_card_id}",
            common.get_image(f"card{next_card_id}.png"),
            self.event_handler.screen,
            17,
            0,
            0,
        )

        old_card = self.condition_cards_group.get_tile_by_id(str(card_id))

        self.condition_cards_group.replace_card(old_card, new_card)

        self.tiles_group.add(new_card)

    def draw_condition_card(self, card_id):
        card = self.non_played_condition_cards.pop(card_id)

        if not card:
            raise NoSuchCardException(card_id, "or is already drawn")

        self.current_drawn_condition_cards[card.id] = card

    def play_card(self, card_id):
        self.event_handler.server_communication_manager.play_condition_card(card_id)

    def remove_played_card(self, card_id):
        card = self.current_drawn_condition_cards.pop(card_id)

        if not card:
            raise NoSuchCardException(card_id, "or is already played or not drawn yet")

        self.played_condition_cards[card_id] = card

        card_tile = self.condition_cards_group.get_tile_by_id(card_id)
        self.tiles_group.remove(card_tile)

    def activate_tile(self, tile, event):
        if tile.name.startswith("condition_card") and event.button == client.LEFT_BUTTON_CLICK:
            self.play_card(int(self.condition_cards_group.get_card_id(tile)))

    def blit(self):
        super().blit()

        if self.condition_cards_group:
            self.condition_cards_group.blit()

        if self.player_number_tiles_group:
            self.player_number_tiles_group.blit()
