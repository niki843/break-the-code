from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull
from utils.enums import GameState
from utils.validate import is_valid_uuid


class GameSession:
    def __init__(self, session_id: str, host_id: str):
        if not is_valid_uuid(host_id):
            raise InvalidPlayerId(host_id)

        self.id = session_id
        self.host_id = host_id
        self.connected_players = [host_id]
        self.state = GameState.PENDING

    def join_player(self, player_id):
        # Check if game session is full
        if len(self.connected_players) > 3:
            raise SessionFull(self.id)

        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

    def start_game(self):
        self.state = GameState.IN_PROGRESS