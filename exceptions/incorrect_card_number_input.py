class IncorrectCardNumberInput(Exception):
    def __init__(
        self,
        player_name,
        message="{} the value for this card is incorrect or is missing",
    ):
        self.player_name = player_name
        self.message = message
        super().__init__(self.message.format(self.player_name))

    def __str__(self):
        return self.message.format(self.player_name)
