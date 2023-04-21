import server


class GameException(Exception):
    def __init__(self, player_id, message, error_type):
        super().__init__(message)
        self.name = server.ERROR_MESSAGE_TYPE
        self.player_id = player_id
        self.message = message
        self.error_type = error_type

    def __str__(self):
        return self.message if self.message else "An error occurred!"
