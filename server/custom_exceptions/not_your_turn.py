from server.custom_exceptions.GameExcpetion import GameException


class NotYourTurnException(GameException):
    MESSAGE = "It's not your turn"
    ERROR_TYPE = "not_your_turn"

    def __init__(self, player_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(player_id, message, error_type)
