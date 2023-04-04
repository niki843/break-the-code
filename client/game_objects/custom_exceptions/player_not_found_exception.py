class PlayerNotFoundException(IndexError):
    def __init__(
        self,
        message="The player you're trying to get does not exist!",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
