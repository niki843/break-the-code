class NotYourTurn(Exception):
    def __init__(self, player_name, message="{} it's not your turn"):
        self.player_name = player_name
        self.message = message
        super().__init__(self.message.format(self.player_name))

    def __str__(self):
        return self.message.format(self.player_name)
