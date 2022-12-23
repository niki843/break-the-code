from types import SimpleNamespace


class ConditionCard(SimpleNamespace):
    def __init__(self, id=None, description=None, additional_info=None, **kwargs):
        self.id = id
        self.description = description
        self.additional_info = additional_info

        super().__init__(**kwargs)
