from server.custom_exceptions import GameExcpetion


class PlayerCardsMissingException(GameExcpetion):
    MESSAGE = "{} hasn't got his cards loaded"
    ERROR_TYPE = "player_cards_missing"

    def __init__(self, player_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(player_id, message, error_type)

    def __str__(self):
        return self.message.format(self.player_id)
