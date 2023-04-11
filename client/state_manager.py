from client.utils import common
from client.utils.singelton import Singleton


class StateManager(Singleton):
    def __init__(self, screen):
        self.player_id, self.username = common.get_or_generate_player_id()
        self.music_volume = 20
        self.resolution = 1
        self.host_id = None
        self.host_username = None
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_type = None
        self.is_player_eliminated = False

    def am_i_host(self):
        return self.host_id and self.player_id == self.host_id

    def set_host(self, host_id, host_name):
        self.host_id = host_id
        self.host_username = host_name

    def change_music_volume(self, new_volume):
        self.music_volume = new_volume

    def change_resolution(self, new_resolution):
        self.resolution = new_resolution
