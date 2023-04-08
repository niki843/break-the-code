import client
from client.utils.singelton import Singleton
from client.ws_client import WebsocketClient

ws_client = WebsocketClient()


async def connect():
    print("Connecting to server")
    await ws_client.connect_to_server()
    print("Connected to server")


async def send_message(message):
    await ws_client.send_server_messages(message)

    print("Message sent")


class ServerCommunicationManager(Singleton):

    GET_CURRENT_GAMES_MESSAGE = '{"type": "get_current_games"}'
    CLOSE_CONNECTION_MESSAGE = '{"type": "close_connection"}'
    EXIT_GAME = '{"type": "exit_game"}'
    START_GAME = '{"type": "start_game"}'
    JOIN_GAME = '{{"type": "join_game", "player_id": "{0}", "player_name": "{1}", "game_session_id": "{2}"}}'
    CREATE_GAME = '{{"type": "new_game", "player_id": "{0}", "player_name": "{1}", "room_name": "{2}"}}'
    PLAY_CARD = '{{"type": "play_tile", "condition_card_id": {0}}}'
    PLAY_CHOICE_CARD = (
        '{{"type": "play_tile", "condition_card_id": {0}, "card_number_choice": {1}}}'
    )

    def __init__(self):
        # Connect to server
        client.LOOP.create_task(connect())

    def get_current_game(self):
        client.LOOP.create_task(send_message(self.GET_CURRENT_GAMES_MESSAGE))

    def close_connection(self):
        client.LOOP.create_task(send_message(self.CLOSE_CONNECTION_MESSAGE))

    def send_join_game_message(self, game_session_id):
        client.LOOP.create_task(
            send_message(
                self.JOIN_GAME.format(
                    client.state_manager.player_id,
                    client.state_manager.username,
                    game_session_id,
                )
            )
        )

    def send_create_game_message(self, game_name):
        client.LOOP.create_task(
            send_message(
                self.CREATE_GAME.format(
                    client.state_manager.player_id,
                    client.state_manager.username,
                    game_name,
                )
            )
        )

    def send_exit_game_message(self):
        client.LOOP.create_task(send_message(self.EXIT_GAME))

    def send_start_game_message(self):
        client.LOOP.create_task(send_message(self.START_GAME))

    def play_condition_card(self, card_id):
        client.LOOP.create_task(send_message(self.PLAY_CARD.format(card_id)))

    def play_choice_condition_card(self, card_id, choice):
        client.LOOP.create_task(
            send_message(self.PLAY_CHOICE_CARD.format(card_id, choice))
        )
