import client
from client.game_objects.custom_exceptions.player_cards_missing import PlayerCardsMissingException
from server.utils.enums import Colors


def first_card(player, number):
    check_player_has_cards(player)

    return get_card_index_list_from_property(player, "number", number)


def second_card(player, number):
    check_player_has_cards(player)

    return get_card_index_list_from_property(player, "number", number)


def third_card(player):
    check_player_has_cards(player)
    return get_card_index_list_from_property(player, "number", 0)


def fourth_card(player):
    check_player_has_cards(player)
    return get_card_index_list_from_property(player, "color", Colors.COLOR_BLACK)


def fifth_card(player):
    check_player_has_cards(player)
    return get_card_index_list_from_property(player, "color", Colors.COLOR_WHITE)


def sixth_card(player):
    check_player_has_cards(player)

    return get_even_or_odd_from_player_tiles(player, 1, "odd")


def seventh_card(player):
    check_player_has_cards(player)
    return get_consecutive_cards(player, "color")


def eight_card(player):
    check_player_has_cards(player)
    start_index = 1
    end_index = 4
    if len(player.get_cards()) == 4:
        end_index = 3

    return get_sum_from_player_tiles(player, start_index, end_index)


def ninth_card(player):
    check_player_has_cards(player)
    start_index = 0
    end_index = 5
    if len(player.get_cards()) == 4:
        end_index = 4

    return get_sum_from_player_tiles(player, start_index, end_index)


def tenth_card(player):
    check_player_has_cards(player)
    return get_consecutive_cards(player, "number")


def eleventh_card(player):
    check_player_has_cards(player)
    return get_sum_for_color(player, Colors.COLOR_BLACK)


def twelfth_card(player):
    check_player_has_cards(player)
    if player.get_cards()[2].number > 4:
        print(f"Player {player.get_name()}s C tile is greater than 4.")
        return True
    print(f"Player {player.get_name()}s C tile is not greater than 4.")
    return False


def thirteenth_card(player):
    check_player_has_cards(player)
    return get_card_index_list_from_property(player, "number", 5)


def fourteenth_card(player):
    check_player_has_cards(player)
    number_list = [x.number for x in player.get_cards()]
    diff = max(number_list) - min(number_list)
    print(
        f"Player {player.get_name()}, has a difference between his highers and lowest card equal to {diff}"
    )
    return diff


def fifteenth_card(player):
    check_player_has_cards(player)

    return get_even_or_odd_from_player_tiles(player, 0, "even")


def sixteenth_card(player, number):
    check_player_has_cards(player)

    return get_card_index_list_from_property(player, "number", number)


def seventeenth_card(player):
    check_player_has_cards(player)
    number_list = [x.number for x in player.get_cards()]

    unique_cards = set(number_list)

    same_number_cards_count = (len(number_list) - len(unique_cards)) * 2

    print(
        f"""Player {player.get_name()}, has {same_number_cards_count} with the same number.
    Bear in mind that the deck of tiles has only a set of 2 with the same number, 
    so this means 2 of one number and 2 of another if the number is 4"""
    )
    return same_number_cards_count


def eighteenth_card(player):
    check_player_has_cards(player)
    start_index = 2
    end_index = 5
    if len(player.get_cards()) == 4:
        start_index = 1
        end_index = 4

    return get_sum_from_player_tiles(player, start_index, end_index)


def nineteenth_card(player):
    check_player_has_cards(player)
    start_index = 0
    end_index = 3

    return get_sum_from_player_tiles(player, start_index, end_index)


def twentieth_card(player):
    check_player_has_cards(player)
    return get_sum_for_color(player, Colors.COLOR_WHITE)


def twenty_first_card(player, number):
    check_player_has_cards(player)

    return get_card_index_list_from_property(player, "number", number)


def get_card_index_list_from_property(player, attr, value):
    player_card_index = []
    for index, card in enumerate(player.get_cards()):
        card_property = getattr(card, attr, client.MISSING_PROPERTY_DEFAULT)
        if card_property == value:
            player_card_index.append(client.CARD_INDEX_TO_LETTER_MAP.get(index))

    if player_card_index:
        print(
            f"Player {player.get_name()}, has a card with {attr} {value} on place\\places {player_card_index}."
        )
        return player_card_index

    print(f"Player {player.get_name()}, hasn't got any cards with {attr} {value}.")
    return player_card_index


def get_consecutive_cards(player, attr):
    player_match_card_indexes = []
    current_match_card_numbers = []
    last_attr = None

    for index, card in enumerate(player.get_cards()):
        card_attr = getattr(card, attr, client.MISSING_PROPERTY_DEFAULT)
        if last_attr is None:
            last_attr = card_attr

        check_value = card.color
        if attr == "number":
            check_value = card.number - 1

        if not current_match_card_numbers or last_attr == check_value:
            current_match_card_numbers.append(client.CARD_INDEX_TO_LETTER_MAP.get(index))
            last_attr = card_attr
            continue

        last_attr = card_attr

        if len(current_match_card_numbers) == 1:
            current_match_card_numbers = [client.CARD_INDEX_TO_LETTER_MAP.get(index)]
            continue

        player_match_card_indexes.append(tuple(current_match_card_numbers))
        current_match_card_numbers = [client.CARD_INDEX_TO_LETTER_MAP.get(index)]

    if len(current_match_card_numbers) >= 2:
        player_match_card_indexes.append(tuple(current_match_card_numbers))

    if player_match_card_indexes:
        print(
            f"Player {player.get_name()}, has a consecutive cards on places {player_match_card_indexes}."
        )
        return player_match_card_indexes

    print(f"Player {player.get_name()}, hasn't got any cards with consecutive numbers.")
    return player_match_card_indexes


def get_sum_from_player_tiles(player, start_index, end_index):
    sum_card = sum([x.number for x in player.get_cards()][start_index:end_index])

    print(f"Player {player.get_name()}, has a sum of {sum_card}.")
    return sum_card


def get_even_or_odd_from_player_tiles(player, eval_num, info_text):
    match_count = 0
    for card in player.get_cards():
        if card.number % 2 == eval_num:
            match_count += 1

    print(f"Player {player.get_name()}, has {match_count} {info_text} tiles.")
    return match_count


def get_sum_for_color(player, color):
    sum_card = 0

    for card in player.get_cards():
        if card.color == color:
            sum_card += card.number

    print(
        f"""Player {player.get_name()}, has a sum of f{sum_card} for his {color} cards. 
        Have in mind that even if the player hasn't got any {color} cards the sum is still 0"""
    )
    return sum_card


def check_player_has_cards(player):
    if not player.get_cards():
        raise PlayerCardsMissingException(player.get_name())


CARD_ID_TO_CONDITION_MAP = {
    1: first_card,
    2: second_card,
    3: third_card,
    4: fourth_card,
    5: fifth_card,
    6: sixth_card,
    7: seventh_card,
    8: eight_card,
    9: ninth_card,
    10: tenth_card,
    11: eleventh_card,
    12: twelfth_card,
    13: thirteenth_card,
    14: fourteenth_card,
    15: fifteenth_card,
    16: sixteenth_card,
    17: seventeenth_card,
    18: eighteenth_card,
    19: nineteenth_card,
    20: twentieth_card,
    21: twenty_first_card,
}
