from types import SimpleNamespace


class Card(SimpleNamespace):
    def __init__(self, number=None, color=None, **kwargs):
        self.number = number
        self.color = color
        super().__init__(**kwargs)
