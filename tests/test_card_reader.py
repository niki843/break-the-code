from types import SimpleNamespace
from unittest.mock import patch

import pytest

from entity.condition_card import Card
from cards.card_conditions import (
    first_card,
    second_card,
    third_card,
    fourth_card,
    fifth_card,
    sixth_card,
    seventh_card,
    eight_card,
    ninth_card,
    eleventh_card,
    twelfth_card,
    thirteenth_card,
    fourteenth_card,
    fifteenth_card,
    sixteenth_card,
    seventeenth_card,
    eighteenth_card,
    nineteenth_card,
    twentieth_card,
    twenty_first_card,
)
from utils.enums import Colors, GameTypes


class TestCardReaderCardConditions:
    @pytest.mark.parametrize("user_input, letter_value", [(8, "d"), (9, "e")])
    def test_first(self, user_input, letter_value):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        with patch("cards.card_conditions.input", lambda x: user_input):
            results = first_card(player)

        assert results
        assert results == [letter_value]

    def test_second(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        results = second_card(player)

        assert results
        assert results == [("a", "b", "c"), ("d", "e")]

    def test_third(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=0),
            ],
        )
        with patch("cards.card_conditions.input", lambda x: 0):
            results = third_card(player)

        assert results
        assert results == ["e"]

    def test_fourth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(color=Colors.COLOR_BLACK),
                Card(color=Colors.COLOR_BLACK),
                Card(color=Colors.COLOR_BLACK),
                Card(color=Colors.COLOR_BLACK),
                Card(color=Colors.COLOR_WHITE),
            ],
        )
        results = fourth_card(player)

        assert results
        assert results == ["a", "b", "c", "d"]

    def test_fifth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_BLACK),
            ],
        )
        results = fifth_card(player)

        assert results
        assert results == ["a", "b", "c", "d"]

    def test_sixth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=0),
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=4),
            ],
        )
        results = sixth_card(player)

        assert results == 2

    def test_seventh(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_WHITE),
                Card(color=Colors.COLOR_BLACK),
                Card(color=Colors.COLOR_BLACK),
            ],
        )
        results = seventh_card(player)

        assert results

    @pytest.mark.parametrize(
        "game_type", [GameTypes.THREE_PLAYER, GameTypes.FOUR_PLAYER]
    )
    def test_eight(self, game_type):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        results = eight_card(player, game_type)

        if game_type == GameTypes.THREE_PLAYER:
            assert results == 13
        else:
            assert results == 5

    @pytest.mark.parametrize(
        "game_type", [GameTypes.THREE_PLAYER, GameTypes.FOUR_PLAYER]
    )
    def test_ninth(self, game_type):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        results = ninth_card(player, game_type)

        if game_type == GameTypes.THREE_PLAYER:
            assert results == 23
        else:
            assert results == 14

    @pytest.mark.parametrize(
        "get_cards, sum_cards",
        [
            (
                lambda: [
                    Card(number=1, color=Colors.COLOR_BLACK),
                    Card(number=2, color=Colors.COLOR_BLACK),
                    Card(number=3, color=Colors.COLOR_WHITE),
                    Card(number=8, color=Colors.COLOR_WHITE),
                    Card(number=9, color=Colors.COLOR_GREEN),
                ],
                3,
            ),
            (
                lambda: [
                    Card(number=1, color=Colors.COLOR_WHITE),
                    Card(number=2, color=Colors.COLOR_WHITE),
                    Card(number=3, color=Colors.COLOR_WHITE),
                    Card(number=8, color=Colors.COLOR_WHITE),
                    Card(number=9, color=Colors.COLOR_GREEN),
                ],
                0,
            ),
        ],
    )
    def test_eleventh(self, get_cards, sum_cards):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            get_cards,
        )
        results = eleventh_card(player)

        assert results == sum_cards

    @pytest.mark.parametrize("c_card, evaluation", [(0, False), (9, True)])
    def test_twelfth(self, c_card, evaluation):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=c_card),
                Card(number=8),
                Card(number=9),
            ],
        )

        result = twelfth_card(player)

        assert result == evaluation

    def test_thirteenth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=5),
                Card(number=5),
                Card(number=4),
            ],
        )

        result = thirteenth_card(player)

        assert result == ["c", "d"]

    def test_fourteenth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )

        result = fourteenth_card(player)

        assert result == 8

    def test_fifteenth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=0),
                Card(number=8),
                Card(number=9),
            ],
        )

        result = fifteenth_card(player)

        assert result == 3

    @pytest.mark.parametrize("user_input, letter_value", [(1, "a"), (2, "b")])
    def test_first(self, user_input, letter_value):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        with patch("cards.card_conditions.input", lambda x: user_input):
            results = sixteenth_card(player)

        assert results
        assert results == [letter_value]

    def test_seventeenth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=1),
                Card(number=3),
                Card(number=9),
                Card(number=9),
            ],
        )
        results = seventeenth_card(player)

        assert results == 4

    @pytest.mark.parametrize("game_type", [GameTypes.FOUR_PLAYER])
    def test_eighteenth(self, game_type):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        results = eighteenth_card(player, game_type)

        if game_type == GameTypes.THREE_PLAYER:
            assert results == 20
        else:
            assert results == 13

    def test_nineteenth(self):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=8),
                Card(number=9),
            ],
        )
        results = nineteenth_card(player)

        assert results == 6

    @pytest.mark.parametrize(
        "get_cards, sum_cards",
        [
            (
                lambda: [
                    Card(number=1, color=Colors.COLOR_BLACK),
                    Card(number=2, color=Colors.COLOR_BLACK),
                    Card(number=3, color=Colors.COLOR_WHITE),
                    Card(number=8, color=Colors.COLOR_WHITE),
                    Card(number=9, color=Colors.COLOR_GREEN),
                ],
                11,
            ),
            (
                lambda: [
                    Card(number=1, color=Colors.COLOR_BLACK),
                    Card(number=2, color=Colors.COLOR_BLACK),
                    Card(number=3, color=Colors.COLOR_BLACK),
                    Card(number=8, color=Colors.COLOR_BLACK),
                    Card(number=9, color=Colors.COLOR_GREEN),
                ],
                0,
            ),
        ],
    )
    def test_twentieth(self, get_cards, sum_cards):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            get_cards,
        )
        results = twentieth_card(player)

        assert results == sum_cards

    @pytest.mark.parametrize("user_input, letter_value", [(3, "c"), (4, "d")])
    def test_twenty_first(self, user_input, letter_value):
        player = SimpleNamespace()
        setattr(player, "get_name", lambda: "test_user")
        setattr(
            player,
            "get_cards",
            lambda: [
                Card(number=1),
                Card(number=2),
                Card(number=3),
                Card(number=4),
                Card(number=9),
            ],
        )
        with patch("cards.card_conditions.input", lambda x: user_input):
            results = twenty_first_card(player)

        assert results
        assert results == [letter_value]
