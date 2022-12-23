import json

import websockets
import copy

from entity.player import Player
from exceptions.invalid_id import InvalidPlayerId
from exceptions.not_your_turn import NotYourTurn
from exceptions.session_full import SessionFull
from utils.game_builder import GameBuilder
from utils.enums import GameState
from utils.validate import is_valid_uuid


class GameSession:
    def __init__(self, session_id: str, player_id: str, player_name: str, websocket):
        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

        self.id = session_id
        # Only the host can start the game
        self.__host = Player(player_id, name=player_name)
        # Needed for playing condition cards, maps player_id to the Player object
        # and sends it directly to the game board
        self.__connected_players = {player_id: self.__host}
        # Needed for starting the game and handing out number cards to the appropriate players
        # also sending the condition card result to all the other players
        self.__connected_player_connections = {self.__host: websocket}
        self.__state = GameState.PENDING
        self.__game_board = None

    def join_player(self, player_id, player_name, websocket):
        # Check if game session is full
        if len(self.__connected_players.keys()) > 3:
            raise SessionFull(self.id)

        if not is_valid_uuid(player_id):
            raise InvalidPlayerId(player_id)

        player = Player(player_id, name=player_name)

        self.__connected_players[player_id] = player
        self.__connected_player_connections[player] = websocket

    async def send_joined_message(self, player_id):
        event = {
            "type": "info",
            "player_id": player_id,
            "message": f"Player {player_id[:7]} has joined",
        }
        websockets.broadcast(
            self.__connected_player_connections.values(), json.dumps(event)
        )

    async def start_game(self):
        self.__state = GameState.IN_PROGRESS

        event = {
            "type": "start_game",
            "message": f"{self.__host.name} started the game",
        }
        websockets.broadcast(
            self.__connected_player_connections.values(), json.dumps(event)
        )

        self.__game_board = GameBuilder(list(self.__connected_players.values()))

        websockets.broadcast(
            self.__connected_player_connections.values(),
            json.dumps(
                {
                    "type": "give_condition_cards",
                    "message": "Giving out condition card ids",
                    "condition_card_ids": [
                        card.id
                        for card in self.__game_board.get_current_condition_cards()
                    ],
                }
            ),
        )

        for player, websocket in self.__connected_player_connections.items():
            await websocket.send(
                json.dumps(
                    {
                        "type": "give_number_cards",
                        "message": "Giving out number cards",
                        "cards": [card.__dict__ for card in player.get_cards()],
                    }
                )
            )

    async def validate_and_play_condition_card(self, websocket, player_id, condition_card_id):
        try:
            self.__game_board.play_condition_card(self.__connected_players[player_id], condition_card_id)
        except NotYourTurn:
            await websocket.send(
                json.dumps(
                    {
                        "type": "error",
                        "message": "It's not your turn!",
                        "error_type": "not_your_turn",
                    }
                )
            )

    def get_players_count(self):
        return len(self.__connected_players)

    def get_state(self):
        return copy.deepcopy(self.__state)

    def get_host(self):
        return self.__host
