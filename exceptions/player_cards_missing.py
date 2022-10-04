

class PlayerCardsMissingException(Exception):

    def __init__(self, player_name, message = "{} hasn't got his cards loaded"):
        self.player_name = player_name
        self.message = message
        super().__init__(self.message.format(self.player_name))

    def __str__(self):
        return self.message.format(self.player_name)
