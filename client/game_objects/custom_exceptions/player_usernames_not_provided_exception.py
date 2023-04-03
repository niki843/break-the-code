class PlayerUsernamesNotProvidedException(IndexError):
    def __init__(
        self,
        message="You are trying to join a game session without providing player usernames!",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
