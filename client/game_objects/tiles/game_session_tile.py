import client

from client.game_objects.tiles.plain_text_box import PlainTextTile
from client.game_objects.tiles.tile import Tile
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common


class GameSessionTile(ToggleTile):
    PLAYER_IMAGE_PATH = "user{0}_1.png"

    def __init__(
        self,
        tile_name,
        next_tile_name,
        surface,
        screen,
        size_percent,
        text_size_percent,
        next_surface,
        active_players,
        player_id_usernames_map,
        game_session_id,
        game_session_name="Unknown",
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        ToggleTile.__init__(
            self,
            tile_name,
            next_tile_name,
            surface,
            screen,
            size_percent,
            next_surface,
            tile_addition_width_percent=tile_addition_width_percent,
            tile_addition_height_percent=tile_addition_height_percent,
        )
        self.player_id_usernames_map = player_id_usernames_map
        self.active_players = active_players
        self.game_session_name = game_session_name
        self.game_session_id = game_session_id
        self.player_usernames = list(player_id_usernames_map.values())
        self.player_image_tiles = []

        self.text_box = PlainTextTile(
            "game_session_name",
            surface,
            screen,
            size_percent,
            game_session_name,
            text_size_percent,
            19,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )

        self.player_images = [
            "user1_1.png",
            "user2_1.png",
            "user3_1.png",
            "user4_1.png",
        ]

    def update_players(self, players_id_name_map):
        self.player_id_usernames_map = players_id_name_map
        self.active_players = len(players_id_name_map.keys())
        self.player_usernames = list(players_id_name_map.values())

    def remove_player(self, player_id):
        self.active_players -= 1
        player_username = self.player_id_usernames_map.pop(player_id)
        self.player_usernames.remove(player_username)

        self.player_image_tiles.pop(-1)
        self.player_images.insert(0, self.PLAYER_IMAGE_PATH.format(len(self.player_image_tiles) + 1))

    def add_player(self, player_id, player_name):
        self.active_players += 1
        self.player_id_usernames_map[player_id] = player_name
        self.player_usernames.append(player_name)

        image_tile = Tile(
            f"player_{len(self.player_image_tiles) + 1}_image",
            common.get_image(self.player_images.pop(0)),
            self.screen,
            3,
        )
        image_tile.rect.right = self.player_image_tiles[-1].rect.left - (self.image.get_width() * 0.01)
        image_tile.rect.centery = self.rect.centery
        self.player_image_tiles.append(image_tile)

    def center_text(self):
        self.text_box.text_rect.left = self.rect.left + (self.screen.get_width() * 0.01)
        self.text_box.text_rect.centery = self.rect.centery

    def set_active_player_images(self):
        position_right = self.rect.right - (self.image.get_width() * 0.01)
        for i in range(0, self.active_players):
            image_tile = Tile(
                f"player_{len(self.player_image_tiles) + 1}_image",
                common.get_image(self.player_images.pop(0)),
                self.screen,
                3,
            )
            image_tile.rect.right = position_right
            image_tile.rect.centery = self.rect.centery

            self.player_image_tiles.append(image_tile)

            position_right = image_tile.rect.left - (self.image.get_width() * 0.01)

    def blit(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(
            self.text_box.text_surface,
            self.text_box.text_rect,
        )
        for player_image in self.player_image_tiles:
            self.screen.blit(player_image.image, player_image.rect)

    def resize(self):
        super().resize()
        if hasattr(self, "text_box"):
            self.text_box.resize()
