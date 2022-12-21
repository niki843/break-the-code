import json

import websockets

from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull
from utils.enums import GameState
from utils.validate import is_valid_uuid


class GameSession:
    def __init__(self, session_id: str, host: str, websocket):
        if not is_valid_uuid(host):
            raise InvalidPlayerId(host)

        self.id = session_id
        self.__host = host, websocket
        self.__connected_player_ids = {host}
        self.__connected_player_connections = {websocket}
        self.state = GameState.PENDING

    def join_player(self, player_id, websocket):
        # Check if game session is full
        if len(self.__connected_player_ids) > 3:
            raise SessionFull(self.id)

        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

        self.__connected_player_ids.add(player_id)
        self.__connected_player_connections.add(websocket)

    def start_game(self):
        self.state = GameState.IN_PROGRESS

    def get_players_count(self):
        return len(self.__connected_player_ids)

    async def send_joined_message(self, player_id):
        event = {
            "type": "info",
            "player_id": player_id,
            "message": f"Player {player_id[:7]} has joined",
        }
        websockets.broadcast(self.__connected_player_connections, json.dumps(event))
