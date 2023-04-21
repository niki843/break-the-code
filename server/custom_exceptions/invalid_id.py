from server.custom_exceptions.game_excpetion import GameException


class InvalidPlayerIdException(GameException):
    MESSAGE = "Player id incorrect"
    ERROR_TYPE = "player_id_not_valid"

    def __init__(self, player_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(player_id, message, error_type)
