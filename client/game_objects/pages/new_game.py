import client
from client.game_objects.cards.card_reader import CardReader
from client.game_objects.custom_exceptions.no_such_card_exception import NoSuchCardException
from client.game_objects.pages.game_window import GameWindow


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.non_played_condition_cards = {}
        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        self.number_cards = []

        self.build()

    def build(self):
        self.build_new_game_background()

    def resize(self):
        super().resize()

    def open(self, **kwargs):
        super().open()
        self.event_handler.server_communication_manager.send_start_game_message()
        cr = CardReader()

        for card in cr.cards:
            self.non_played_condition_cards[card.id] = card

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
