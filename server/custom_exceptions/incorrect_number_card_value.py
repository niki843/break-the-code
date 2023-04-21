from server.custom_exceptions.GameExcpetion import GameException


class IncorrectNumberCardValueException(GameException):
    MESSAGE = "The card you played should be from two characters first char 0-Black, 1-White, 2-Green and second one for the number"
    ERROR_TYPE = "incorrect_number_card_value"

    def __init__(
        self,
        player_id,
        message=MESSAGE,
        error_type=ERROR_TYPE,
    ):
        super().__init__(player_id, message, error_type)
