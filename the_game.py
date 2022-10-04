import random

from constants import NUMBER_CARDS_COUNT, \
    NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS, NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS, GameTypes, Colors
from types import SimpleNamespace

from player import Player

GAME_TYPE = None


def build_game():
    players_count = int(input("Please input number of players:"))
    while players_count < 2 or players_count > 4:
        players_count = int(input("Sorry the number of players could be between 2-4 players. Please enter the amount "
                                  "of players:"))

    players = populate_players(players_count)

    numbers = create_number_cards()
    populate_number_cards(numbers)

    hand_out_number_cards_to_players(players, numbers)


def create_number_cards():
    number_cards = []
    for index in range(1, NUMBER_CARDS_COUNT + 1):
        number_cards.append(SimpleNamespace())
    return number_cards


def populate_number_cards(numbers: list):
    for index in range(0, len(numbers)):
        if index == 5 or index == 15:
            setattr(numbers[index], 'color', Colors.COLOR_GREEN)
            setattr(numbers[index], 'number', index % 10)
            continue

        if index <= 9:
            setattr(numbers[index], 'color', Colors.COLOR_WHITE)
            setattr(numbers[index], 'number', index)
            continue
        setattr(numbers[index], 'color', Colors.COLOR_BLACK)
        setattr(numbers[index], 'number', index % 10)


def populate_players(players_count):
    global GAME_TYPE
    players = []

    for i in range(players_count):
        players.append(Player(i, f'test_name{i}'))

    GAME_TYPE = GameTypes(len(players))

    return players


def hand_out_number_cards_to_players(players, cards):
    number_cards_amount = NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS \
        if len(players) == 4 else NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS
    for player in players:
        current_player_numbers = []
        for i in range(number_cards_amount):
            current_player_numbers.append(cards.pop(random.randint(0, len(cards) - 1)))
        player.update_numbers(current_player_numbers)


if __name__ == '__main__':
    build_game()
