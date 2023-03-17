class IncorrectAmountOfCardsInGuess(Exception):
    def __init__(
        self,
        player_name,
        message="{} the cards you tried to guess is not the right amount for the game, 3 for Four players, 4 for Three",
    ):
        self.player_name = player_name
        self.message = message
        super().__init__(self.message.format(self.player_name))

    def __str__(self):
        return self.message.format(self.player_name)
