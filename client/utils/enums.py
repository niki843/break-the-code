from enum import IntEnum, Enum, auto


class Colors(IntEnum):
    COLOR_BLACK = 0
    COLOR_WHITE = 1
    COLOR_GREEN = 2

    def __str__(self):
        if self.value == Colors.COLOR_BLACK:
            return "black"
        elif self.value == Colors.COLOR_WHITE:
            return "white"
        else:
            return "green"


class Position(Enum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto

    def __str__(self):
        if self.value == Position.LEFT:
            return "left"
        elif self.value == Position.RIGHT:
            return "right"
        elif self.value == Position.TOP:
            return "top"
        else:
            return "bottom"
