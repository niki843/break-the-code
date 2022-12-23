from enum import IntEnum

MISSING_PROPERTY_DEFAULT = -1
NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS = 5
NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS = 4
NUMBER_CARDS_COUNT = 20
CARD_INDEX_TO_LETTER_MAP = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}


class GameTypes(IntEnum):
    TWO_PLAYER = 2
    THREE_PLAYER = 3
    FOUR_PLAYER = 4


class Colors(IntEnum):
    COLOR_WHITE = 0
    COLOR_BLACK = 1
    COLOR_GREEN = 2

    def __str__(self):
        if self.value == Colors.COLOR_BLACK:
            return "Black"
        elif self.value == Colors.COLOR_WHITE:
            return "White"
        else:
            return "Green"
