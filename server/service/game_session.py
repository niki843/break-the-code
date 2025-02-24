import json

import websockets
import copy
import server

from server import custom_exceptions
from server.entity.player import Player
from server.utils.game_builder import GameBuilder
from server.utils.enums import GameState, EndGame, PlayerStatus
from server.utils.validate import is_valid_uuid


class GameSession:
    GAME_SESSION_CLOSED_MESSAGE_TYPE = "game_session_closed"
    GAME_SESSION_CLOSED_WHEN_PENDING_MESSAGE = "All players disconnected deleting game session"

    def __init__(self, session_id: str, player_id: str, player_name: str, websocket, room_name):
        if not is_valid_uuid(player_id):
            raise custom_exceptions.InvalidPlayerIdException(player_id)

        self.id = session_id
        self.room_name = room_name
        # Only the host can start the game
        self.__host = Player(player_id, name=player_name)
        # Needed for playing condition cards, maps player_id to the Player object
        # and sends it directly to the game board
        self.__connected_players = {player_id: self.__host}
        self.__connected_players_status = {player_id: PlayerStatus.ONLINE}
        # Needed for starting the game and handing out number cards to the appropriate players
        # also sending the condition card result to all the other players
        self.__connected_player_connections = {self.__host: websocket}
        self.__state = GameState.PENDING
        self.__game_board = None
        self.__current_player_at_hand_id = list(self.__connected_players.keys())[0]
        self.__played_condition_cards_and_results = []

    async def join_player(self, player_id, player_name, websocket):
        # Check if player is trying to reconnect
        if (
            player_id in self.__connected_players.keys()
            and self.get_player_status_by_id(player_id) != PlayerStatus.ONLINE
        ):
            player = self.__connected_players.get(player_id)
            self.__connected_players_status[player_id] = PlayerStatus.ONLINE
            self.__connected_player_connections[player] = websocket
            await self.send_current_cards_message_to_reconnected_player(
                websocket, player
            )
            return

        if self.__state != GameState.PENDING:
            raise custom_exceptions.SessionInProgress(self.id)

        # Check if game session is full
        if len(self.__connected_players.keys()) > 3:
            raise custom_exceptions.SessionFullException(self.id)

        if not is_valid_uuid(player_id):
            raise custom_exceptions.InvalidPlayerIdException(player_id)

        player = Player(player_id, name=player_name)

        self.__connected_players[player_id] = player
        self.__connected_player_connections[player] = websocket
        self.__connected_players_status[player_id] = PlayerStatus.ONLINE

    async def send_joined_message(self, player_id, player_name):
        event = {
            "type": "player_joined",
            "player_name": player_name,
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

    async def play_condition_card_and_change_player(
        self, player_id, condition_card_id, card_number_choice
    ):
        self.validate_current_player(player_id)

        if (
            condition_card_id in server.CARDS_REQUIRING_USER_INPUT_MAP.keys()
            and card_number_choice
            not in server.CARDS_REQUIRING_USER_INPUT_MAP[condition_card_id]
        ):
            raise custom_exceptions.IncorrectConditionCardAdditionalInputException(player_id)

        card, new_card, end_game = self.__game_board.play_condition_card(
            self.__connected_players[player_id], condition_card_id
        )

        if end_game == EndGame.ALL_CARDS_PLAYED:
            # The game should end after everyone receives one final guess
            websockets.broadcast(
                self.__connected_player_connections.values(),
                json.dumps(
                    {
                        "type": "warning_all_cards_played",
                        "message": "All the condition cards have been played, each player has a turn to try to guess!",
                    }
                ),
            )
            self.__state = GameState.END_ALL_CARDS_PLAYED

        next_card_id = new_card.id if new_card else None

        event = {
            "type": "card_condition_result",
            "message": "Returning results from played card condition",
            "card_id": card.id,
            "next_card_id": next_card_id,
            "card_condition": card.description,
            "player_results": [],
        }

        self.__played_condition_cards_and_results.append(event)

        for player, websocket_value in self.__connected_player_connections.items():
            if player.get_id() != player_id:
                if card.has_user_choice:
                    matching_card_condition = card.check_condition(
                        player, card_number_choice
                    )
                    event["card_number_choice"] = card_number_choice
                else:
                    matching_card_condition = card.check_condition(player)
                event.get("player_results").append({"player_id": player.get_id(), "player_name": player.get_name(), "matching_cards": matching_card_condition})

        # change the current player at hand to the next in line
        self.next_player()

        websockets.broadcast(
            self.__connected_player_connections.values(), json.dumps(event)
        )
        # await self.give_out_condition_cards()

    async def send_message_to_all_others(self, player_id, message_content):
        event = {
            "type": "chat_message",
            "playerid": player_id,
            "message": f"{message_content}",
        }
        websockets.broadcast(
            self.get_player_connection_without_id(player_id), json.dumps(event)
        )

    async def guess_number_and_change_player(self, player_id, player_guess):
        self.validate_current_player(player_id)
        player = self.__connected_players[self.__current_player_at_hand_id]

        is_guess_correct = self.__game_board.guess_cards(player_id, player_guess)

        if is_guess_correct:
            self.end_game_and_send_messages(player)
            print(f"Player {player.get_name()} wins!")
            return

        player.is_eliminated = True
        websockets.broadcast(
            self.__connected_player_connections.values(),
            json.dumps(
                {
                    "type": "player_eliminated",
                    "message": f"{player.get_name()} guessed the wrong cards and is eliminated",
                    "player_id": str(self.__current_player_at_hand_id),
                }
            ),
        )
        print(f"Incorrect guess {self.__current_player_at_hand_id} is eliminated")

        if self.are_all_players_eliminated():
            self.end_game_and_send_messages()
            return

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

        current_player_index = (players_list.index(self.__current_player_at_hand_id) + 1) - len(players_list)
        self.__current_player_at_hand_id = players_list[current_player_index]

        if self.__connected_players.get(self.__current_player_at_hand_id).is_eliminated:
            self.next_player()
        print(f"Player at hand: {self.__current_player_at_hand_id}")

    def validate_current_player(self, player_id):
        if player_id != self.__current_player_at_hand_id:
            raise custom_exceptions.NotYourTurnException(player_id)

    def end_game_and_send_messages(self, player=None):
        self.__state = GameState.END
        if player:
            websockets.broadcast(
                self.__connected_player_connections.values(),
                json.dumps(
                    {
                        "type": "end_game",
                        "message": f"Winner {player.get_name()}",
                        "winner_id": player.get_id(),
                    }
                ),
            )
        else:
            websockets.broadcast(
                self.__connected_player_connections.values(),
                json.dumps(
                    {
                        "type": "end_game_no_winners",
                        "message": f"No winners",
                    }
                ),
            )

    def replace_host(self, player_id):
        if self.__host.get_id() != player_id:
            return

        player = self.__connected_players.get(player_id)
        self.__connected_player_connections.pop(player)
        self.__connected_players.pop(player_id)
        self.__connected_players_status.pop(player_id)

        new_host = list(self.__connected_players.values())[0]
        self.__host = new_host
        self.__current_player_at_hand_id = new_host.get_id()

        self.send_replaced_host_message(new_host)

    def are_all_players_disconnected(self):
        return len([player for player, status in self.__connected_players_status.items() if status == PlayerStatus.ONLINE]) <= 1

    def get_players_count(self):
        return len(self.__connected_players)

    def get_state(self):
        return copy.deepcopy(self.__state)

    def get_host(self):
        return self.__host

    def get_room_name(self):
        return self.room_name

    def get_current_player(self):
        return self.__connected_players[self.__current_player_at_hand_id]

    def get_player_name_by_id(self, player_id):
        return self.__connected_players.get(player_id).get_name()

    def get_player_connection_without_id(self, player_id):
        ws = []
        for player, websocket in self.__connected_player_connections.items():
            if player.get_id() != player_id:
                ws.append(websocket)
        return ws

    def get_player_status_by_id(self, player_id):
        return self.__connected_players_status.get(player_id)

    def get_player_by_id(self, player_id):
        return self.__connected_players.get(player_id)

    def get_player_id_name_map(self):
        return {player_id: player.get_name() for player_id, player in self.__connected_players.items()}

    def player_reconnected_broadcast(self, player_id):
        event = {
            "type": "player_reconnected",
            "message": f"Player {self.get_player_name_by_id(player_id)} reconnected.",
            "player_id": str(player_id),
        }

        websockets.broadcast(
            self.__connected_player_connections.values(),
            json.dumps(event),
        )

    def player_not_reconnect_broadcast(self, player_id):
        event = {
            "type": "player_removed",
            "message": f"Player {self.get_player_name_by_id(player_id)} did not connect replacing with bot.",
            "player_id": str(player_id),
        }

        websockets.broadcast(
            self.get_player_connection_without_id(player_id),
            json.dumps(event),
        )

    def player_disconnected_broadcast(self, player_id):
        event = {
            "type": "player_disconnected",
            "message": f"Player {self.get_player_name_by_id(player_id)} disconnected. Waiting 30 seconds to reconnect.",
            "player_id": str(player_id),
        }

        websockets.broadcast(
            self.get_player_connection_without_id(player_id),
            json.dumps(event),
        )

    def send_replaced_host_message(self, player):
        event = {
            "type": "host_disconnected",
            "message": f"New host {player.get_name()}",
            "player_id": str(player.get_id()),
        }

        websockets.broadcast(
            self.__connected_player_connections.values(),
            json.dumps(event),
        )

    def set_player_disconnected(self, player_id):
        try:
            self.__connected_players_status[player_id] = PlayerStatus.DISCONNECTED
        except KeyError:
            return False

        return True

    def remove_player(self, player_id):
        player = self.__connected_players.pop(player_id)
        self.__connected_player_connections.pop(player)
        self.__connected_players_status.pop(player_id)

    def have_all_players_disconnected(self):
        return not any(
            player_status == PlayerStatus.ONLINE
            for player_status in self.__connected_players_status.values()
        )

    def are_all_players_eliminated(self):
        return all([player.is_eliminated for player in self.__connected_players.values()])

    async def send_current_cards_message_to_reconnected_player(self, websocket, player):
        await websocket.send(
            json.dumps(
                {
                    "type": "give_number_cards",
                    "message": "Giving out number cards",
                    "cards": [card.__dict__ for card in player.get_cards()],
                }
            )
        )

        await websocket.send(
            json.dumps(
                {
                    "type": "give_condition_cards",
                    "message": "Giving out condition card ids",
                    "condition_card_ids": [
                        card.id
                        for card in self.__game_board.get_current_condition_cards()
                    ],
                }
            )
        )

        await websocket.send(
            json.dumps(
                {
                    "type": "give_played_condition_cards",
                    "message": "Giving out condition card that were played and results",
                    "results": self.__played_condition_cards_and_results,
                }
            )
        )
