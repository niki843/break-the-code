class InvalidPlayerId(Exception):
    def __init__(self, player_id, message="Player id `{}` is not correct"):
        self.player_id = player_id
        self.message = message
        super().__init__(self.message.format(self.player_id))
