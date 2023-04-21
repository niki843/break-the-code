from server.custom_exceptions.game_excpetion import GameException


class IncorrectAmountOfCardsInGuessException(GameException):
    MESSAGE = "The cards you tried to guess is not the right amount for the game, 4 for Four players, 5 for Three"
    ERROR_TYPE = "incorrect_amount_of_cards"

    def __init__(
        self,
        player_name,
        message=MESSAGE,
        error_type=ERROR_TYPE
    ):
        super().__init__(player_name, message, error_type)
