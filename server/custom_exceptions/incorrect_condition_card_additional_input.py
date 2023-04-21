from server.custom_exceptions.game_excpetion import GameException


class IncorrectConditionCardAdditionalInputException(GameException):
    MESSAGE = "The additional value for this condition card is incorrect or is missing"
    ERROR_TYPE = "incorrect_card_number_input"

    def __init__(
        self,
        player_id,
        message=MESSAGE,
        error_type=ERROR_TYPE
    ):
        super().__init__(player_id, message, error_type)
