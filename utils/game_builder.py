import random
from copy import deepcopy
from types import SimpleNamespace

from cards.card_reader import CardReader
from utils.enums import Colors, GameTypes


# Setting the GameBuilder to Singleton will prevent re-loading the game assets like cards, players etc.
from exceptions.not_your_turn import NotYourTurn


class GameBuilder:
    def __init__(self, players: list):
        self.players = players
        self.condition_cards, self.number_cards = self.build_game()
        self.game_type = GameTypes(len(players))
        self.__current_condition_cards = random.sample(self.condition_cards, 6)
        self.__current_player_at_hand = players[0]

    def build_game(self):
        number_cards = self.create_number_cards()
        self.populate_number_cards(number_cards)

        self.hand_out_number_cards_to_players(self.players, number_cards)
        condition_cards = CardReader().cards
        return condition_cards, number_cards

    def get_current_condition_cards(self):
        return deepcopy(self.__current_condition_cards)

    def play_condition_card(self, player, condition_card_id):
        if player != self.__current_player_at_hand:
            raise NotYourTurn(player.get_name())

    @staticmethod
    def create_number_cards():
        number_cards = []
        for index in range(1, constants.NUMBER_CARDS_COUNT + 1):
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
            constants.NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS
            if len(players) == 4
            else constants.NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS
        )
        for player in players:
            current_player_numbers = []
            for i in range(number_cards_amount):
                current_player_numbers.append(
                    cards.pop(random.randint(0, len(cards) - 1))
                )
            current_player_numbers.sort(key=lambda x: x.number)
            player.update_number_cards(current_player_numbers)
