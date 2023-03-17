class ScreenResolutionSliderException(Exception):
    def __init__(
        self,
        message="The slider that you're using has more values than the supported resolutions",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
