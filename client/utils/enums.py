from enum import IntEnum, auto


class Colors(IntEnum):
    COLOR_BLACK = auto()
    COLOR_WHITE = auto()
    COLOR_GREEN = auto()

    def __str__(self):
        if self.value == Colors.COLOR_BLACK:
            return "Black"
        elif self.value == Colors.COLOR_WHITE:
            return "White"
        else:
            return "Green"