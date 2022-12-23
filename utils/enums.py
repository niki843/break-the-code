from enum import Enum, IntEnum


class GameState(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    END = 3


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
