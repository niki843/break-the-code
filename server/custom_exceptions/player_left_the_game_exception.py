class PlayerLeftTheGameException(Exception):
    def __init__(self, player_id, message="Player with id `{}` left the game."):
        self.player_id = player_id
        self.message = message
        super().__init__(self.message.format(self.player_id))
