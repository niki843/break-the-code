import random
from types import SimpleNamespace

from constants import (
    NUMBER_CARDS_COUNT,
    Colors,
    GameTypes,
    NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS,
    NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS,
)
from cards.card_reader import CardReader


# Setting the GameBuilder to Singleton will prevent re-loading the game assets like cards, players etc.
class GameBuilder:
    def __init__(self, players: set):
        self.game_type = None
        self.players = players
        self.cards, self.players, self.number_cards = self.build_game()
        self.game_type = GameTypes(len(players))

    def build_game(self):
        number_cards = self.create_number_cards()
        self.populate_number_cards(number_cards)

        self.hand_out_number_cards_to_players(self.players, number_cards)
        cards = CardReader().cards
        return cards, self.players, number_cards

    @staticmethod
    def create_number_cards():
        number_cards = []
        for index in range(1, NUMBER_CARDS_COUNT + 1):
            number_cards.append(SimpleNamespace())
        return number_cards

    @staticmethod
    def populate_number_cards(numbers: list):
        for index in range(0, len(numbers)):
            if index == 5 or index == 15:
                setattr(numbers[index], "color", Colors.COLOR_GREEN)
                setattr(numbers[index], "number", index % 10)
                continue

            if index <= 9:
                setattr(numbers[index], "color", Colors.COLOR_WHITE)
                setattr(numbers[index], "number", index)
                continue
            setattr(numbers[index], "color", Colors.COLOR_BLACK)
            setattr(numbers[index], "number", index % 10)

    @staticmethod
    def hand_out_number_cards_to_players(players, cards):
        number_cards_amount = (
            NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS
            if len(players) == 4
            else NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS
        )
        for player in players:
            current_player_numbers = []
            for i in range(number_cards_amount):
                current_player_numbers.append(
                    cards.pop(random.randint(0, len(cards) - 1))
                )
            current_player_numbers.sort(key=lambda x: x.number)
            player.update_number_cards(current_player_numbers)
