from server.custom_exceptions.game_excpetion import GameException


class PlayerLeftTheGameException(GameException):
    MESSAGE = "Player with id `{}` left the game."
    ERROR_TYPE = "player_left"

    def __init__(self, player_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(player_id, message, error_type)

    def __str__(self):
        return self.message.format(self.player_id)
