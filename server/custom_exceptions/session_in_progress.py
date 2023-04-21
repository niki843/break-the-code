from server.custom_exceptions.GameExcpetion import GameException


class SessionInProgress(GameException):
    MESSAGE = "Session with id `{}` is already in progress."
    ERROR_TYPE = "session_in_progress"

    def __init__(self, session_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(session_id, message, error_type)

    def __str__(self):
        return self.message.format(self.player_id)
