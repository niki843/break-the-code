import json

import websockets
import copy

from entity.player import Player
from exceptions.incorrect_card import IncorrectCardPlayed
from exceptions.invalid_id import InvalidPlayerId
from exceptions.not_your_turn import NotYourTurn
from exceptions.session_full import SessionFull
from utils.game_builder import GameBuilder
from utils.enums import GameState, EndGame
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
        self.__current_player_at_hand = list(self.__connected_players.keys())[0]

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

        await self.give_out_condition_cards()

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

    async def play_condition_card_and_change_player(self, player_id, condition_card_id):
        self.validate_current_player(player_id)

        card = self.__game_board.play_condition_card(
            self.__connected_players[player_id], condition_card_id
        )

        # change the current player at hand to the next in line
        self.next_player()

        if card == EndGame.ALL_CARDS_PLAYED:
            # TODO: Implement end game and request one final turn for each to guess before end
            self.end_game_and_send_messages()

        event = {
            "type": "card_condition_result",
            "message": "Returning results from played card condition",
            "card_condition": card.description,
        }

        for player, websocket_value in self.__connected_player_connections.items():
            if player.get_id() != player_id:
                matching_card_condition = card.check_condition(player)
                event[player.get_id()] = matching_card_condition

        websockets.broadcast(
            self.__connected_player_connections.values(), json.dumps(event)
        )
        await self.give_out_condition_cards()

    async def guess_number_and_change_player(self, player_id, player_guess):
        self.validate_current_player(player_id)

        is_guess_correct = self.__game_board.guess_cards(player_id, player_guess)

        if is_guess_correct:
            # TODO: Implement end game
            self.end_game_and_send_messages()
            print(f"Player {self.__current_player_at_hand} wins!")

        # TODO: Implement player can't guess anymore
        print(f"Incorrect guess {self.__current_player_at_hand} is eliminated")

        # change the current player at hand to the next in line
        self.next_player()

    async def give_out_condition_cards(self):
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

    def next_player(self):
        players_list = list(self.__connected_players.keys())

        current_player_index = players_list.index(self.__current_player_at_hand) + 1

        self.__current_player_at_hand = players_list[
            current_player_index if current_player_index < len(players_list) else 0
        ]

    def validate_current_player(self, player_id):
        if player_id != self.__current_player_at_hand:
            raise NotYourTurn(player_id)

    def end_game_and_send_messages(self):
        pass

    def get_players_count(self):
        return len(self.__connected_players)

    def get_state(self):
        return copy.deepcopy(self.__state)

    def get_host(self):
        return self.__host
