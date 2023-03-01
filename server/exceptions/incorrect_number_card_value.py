class IncorrectNumberCardValue(Exception):
    def __init__(
        self,
        player_name,
        message="{} the card you played should be from two characters first char 0-Black, 1-White, 2-Green and second one for the number",
    ):
        self.player_name = player_name
        self.message = message
        super().__init__(self.message.format(self.player_name))

    def __str__(self):
        return self.message.format(self.player_name)
