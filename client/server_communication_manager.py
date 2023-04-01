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
    JOIN_GAME = '{{"type": "join_game", "player_id": "{0}", "player_name": "{1}", "game_session_id": "{2}"}}'

    def __init__(self, player_username, player_id):
        self.player_username = player_username
        self.player_id = player_id

        # Connect to server
        client.LOOP.create_task(connect())

    def get_current_game(self):
        client.LOOP.create_task(send_message(self.GET_CURRENT_GAMES_MESSAGE))

    def close_connection(self):
        client.LOOP.create_task(send_message(self.CLOSE_CONNECTION_MESSAGE))

    def send_join_game_message(self, game_session_id):
        client.LOOP.create_task(send_message(self.JOIN_GAME.format(self.player_id, self.player_username, game_session_id)))
