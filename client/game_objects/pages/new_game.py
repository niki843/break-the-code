import client
from client.game_objects.cards.card_reader import CardReader
from client.game_objects.custom_exceptions.no_such_card_exception import NoSuchCardException
from client.game_objects.groups.condition_cards_group import ConditionCardsGroup
from client.game_objects.pages.game_window import GameWindow


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.non_played_condition_cards = {}
        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        self.number_cards = []

        self.condition_cards_group = None

        self.build()

    def build(self):
        self.build_new_game_background()

    def resize(self):
        super().resize()

        self.set_condition_cards_size()

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

    def open(self, **kwargs):
        super().open()
        self.event_handler.server_communication_manager.send_start_game_message()
        cr = CardReader()

        for card in cr.cards:
            self.non_played_condition_cards[card.id] = card

    def load_condition_cards(self, card_ids):
        for card_id in card_ids:
            self.current_drawn_condition_cards[card_id] = self.non_played_condition_cards.pop(card_id)

        self.build_draw_pile(self.current_drawn_condition_cards.values())

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

    def activate_tile(self, tile, event):
        if tile.name == "condition_card" and event.button == client.LEFT_BUTTON_CLICK:
            pass

    def blit(self):
        super().blit()

        if self.condition_cards_group:
            self.condition_cards_group.blit()
