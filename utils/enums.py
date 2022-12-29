from enum import Enum, IntEnum


class GameState(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    END = 3
    # The game is ending after all players receive one try to guess
    END_ALL_CARDS_PLAYED = 3


class EndGame(Enum):
    ALL_CARDS_PLAYED = 0


class GameTypes(IntEnum):
    TWO_PLAYER = 2
    THREE_PLAYER = 3
    FOUR_PLAYER = 4


class Colors(IntEnum):
    COLOR_WHITE = 1
    COLOR_BLACK = 0
    COLOR_GREEN = 2

    def __str__(self):
        if self.value == Colors.COLOR_BLACK:
            return "Black"
        elif self.value == Colors.COLOR_WHITE:
            return "White"
        else:
            return "Green"
