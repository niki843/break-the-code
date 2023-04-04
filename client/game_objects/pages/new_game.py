import client
from client.game_objects.cards.card_reader import CardReader
from client.game_objects.custom_exceptions.no_such_card_exception import NoSuchCardException
from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.tile import Tile
from client.utils import common


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.non_played_condition_cards = {}
        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        self.number_cards = []

        self.draw_pile_tile = None

        self.build()

    def build(self):
        self.build_new_game_background()

        self.build_draw_pile()

    def resize(self):
        super().resize()

        self.set_draw_pile_size()

    def build_draw_pile(self):
        surface = common.get_image("card_back.png")

        self.draw_pile_tile = Tile(
            "draw_pile",
            surface,
            self.event_handler.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            0,
            0,
        )

        self.set_draw_pile_size()

    def set_draw_pile_size(self):
        if not self.draw_pile_tile:
            return

        self.draw_pile_tile.resize()
        self.draw_pile_tile.rect.centerx = self.event_handler.screen_rect.centerx
        self.draw_pile_tile.rect.centery = self.event_handler.screen_rect.centery

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

        self.event_handler.screen.blit(self.draw_pile_tile.image, self.draw_pile_tile.rect)
