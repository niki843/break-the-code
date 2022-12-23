from types import SimpleNamespace


class ConditionCard(SimpleNamespace):
    def __init__(self, card_id=None, description=None, additional_info=None, **kwargs):
        self.card_id = card_id
        self.description = description
        self.additional_info = additional_info

        super().__init__(**kwargs)
