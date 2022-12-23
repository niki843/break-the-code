import json

import websockets
import copy

from entity.player import Player
from exceptions.invalid_id import InvalidPlayerId
from exceptions.session_full import SessionFull
from game_builder import GameBuilder
from utils.enums import GameState
from utils.validate import is_valid_uuid


class GameSession:
    def __init__(self, session_id: str, player_id: str, player_name: str, websocket):
        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

        self.id = session_id
        self.__host = Player(player_id, name=player_name)
        self.__connected_players = [self.__host]
        self.__connected_player_connections = {self.__host: websocket}
        self.__state = GameState.PENDING
        self.__game_board = None

    def join_player(self, player_id, player_name, websocket):
        # Check if game session is full
        if len(self.__connected_players) > 3:
            raise SessionFull(self.id)

        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

        player = Player(player_id, name=player_name)

        self.__connected_players.append(player)
        self.__connected_player_connections[player] = websocket

    async def send_joined_message(self, player_id):
        event = {
            "type": "info",
            "player_id": player_id,
            "message": f"Player {player_id[:7]} has joined",
        }
        websockets.broadcast(self.__connected_player_connections.values(), json.dumps(event))

    async def start_game(self):
        self.__state = GameState.IN_PROGRESS

        event = {
            "type": "start_game",
            "message": f"{self.__host.name} started the game",
        }
        websockets.broadcast(self.__connected_player_connections.values(), json.dumps(event))

        self.__game_board = GameBuilder(self.__connected_players)

        for player, websocket in self.__connected_player_connections.items():
            await websocket.send(
                json.dumps(
                    {
                        "type": "give_number_cards",
                        "cards": [card.__dict__ for card in player.get_cards()],
                    }
                )
            )

    # def choose_card(self):
    #     self.__game_board.current_condition_cards

    def get_players_count(self):
        return len(self.__connected_players)

    def get_state(self):
        return copy.deepcopy(self.__state)

    def get_host(self):
        return self.__host
