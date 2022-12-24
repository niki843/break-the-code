import random
import constants
from copy import deepcopy
from types import SimpleNamespace

from cards.card_reader import CardReader
from exceptions.incorrect_amount_of_cards_in_guess import IncorrectAmountOfCardsInGuess
from exceptions.incorrect_card import IncorrectCardPlayed
from exceptions.incorrect_number_card_value import IncorrectNumberCardValue
from utils.enums import Colors, GameTypes, EndGame

# Setting the GameBuilder to Singleton will prevent re-loading the game assets like cards, players etc.
from exceptions.not_your_turn import NotYourTurn


class GameBuilder:
    def __init__(self, players: list):
        self.players = players
        self.condition_cards, self.number_cards = self.build_game()
        self.game_type = GameTypes(len(players))
        self.__current_condition_cards = random.sample(self.condition_cards, 6)
        self.condition_cards = [
            card
            for card in self.condition_cards
            if card not in self.__current_condition_cards
        ]

    def build_game(self):
        number_cards = self.create_number_cards()
        self.populate_number_cards(number_cards)

        self.hand_out_number_cards_to_players(self.players, number_cards)
        condition_cards = CardReader().cards
        return condition_cards, number_cards

    def get_current_condition_cards(self):
        return deepcopy(self.__current_condition_cards)

    def play_condition_card(self, player, condition_card_id):

        if not any(
            condition_card_id == card.id for card in self.__current_condition_cards
        ):
            raise IncorrectCardPlayed(player.get_id())

        for card in self.__current_condition_cards:
            if card.id == condition_card_id:
                self.__current_condition_cards.remove(card)
                # In the case that all the cards are drawn the game should play until the last card is called
                if len(self.condition_cards) == 0:
                    return card

                new_card = random.choice(self.condition_cards)
                self.__current_condition_cards.append(new_card)

                self.condition_cards.remove(new_card)

                return card

        # if no cards left in current_cards send end game message
        return EndGame.ALL_CARDS_PLAYED

    def guess_cards(self, player_id, player_guess):
        if (self.game_type == GameTypes.FOUR_PLAYER and len(player_guess) != 4) or (
            self.game_type == GameTypes.THREE_PLAYER and len(player_guess) != 5
        ):
            raise IncorrectAmountOfCardsInGuess(player_id)

        is_correct_guess = True
        for count, card in enumerate(self.number_cards):
            if len(player_guess[count]) != 2:
                raise IncorrectNumberCardValue(player_id)

            if (
                int(player_guess[count][0]) != card.color.value
                or int(player_guess[count][1]) != card.number
            ):
                is_correct_guess = False

        return is_correct_guess

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

            player.order_cards()
            current_player_numbers.sort(key=lambda x: x.number)
            player.update_number_cards(current_player_numbers)
