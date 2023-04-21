from server.custom_exceptions.GameExcpetion import GameException


class SessionFullException(GameException):
    MESSAGE = "The game session is full"
    ERROR_TYPE = "session_full"

    def __init__(self, session_id, message=MESSAGE, error_type=ERROR_TYPE):
        super().__init__(session_id, message, error_type)
