from types import SimpleNamespace


class ConditionCard(SimpleNamespace):
    def __init__(
        self,
        id=None,
        description=None,
        has_user_choice=None,
        additional_info=None,
        positive_condition_message=None,
        negative_condition_message=None,
        choices=None,
        **kwargs
    ):
        self.id = id
        self.description = description
        self.has_user_choice = has_user_choice
        self.additional_info = additional_info
        self.positive_condition_message = positive_condition_message
        self.negative_condition_message = negative_condition_message
        self.choices = choices

        super().__init__(**kwargs)
