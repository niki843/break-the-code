from client.game_objects.cards.card_reader import CardReader
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

    def blit(self):
        super().blit()
