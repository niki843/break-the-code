from server.custom_exceptions.GameExcpetion import GameException


class CardNotDrawnException(GameException):
    MESSAGE = "The card you requested is not in the current drawn cards"
    ERROR_TYPE = "incorrect_card_player"

    def __init__(self, player_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(player_id, message, error_type)
