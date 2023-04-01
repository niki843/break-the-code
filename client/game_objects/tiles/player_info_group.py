import pygame

from client.game_objects.custom_exceptions.player_limit_exceeded_exception import PlayerLimitExceededException
from client.game_objects.tiles.plain_text_box import PlainTextTile
from client.game_objects.tiles.tile import Tile
from client.utils import common


class PlayerInfoGroup:
    MAX_PLAYERS_IN_GROUP = 4
    player_images = [
        "user1_1.png",
        "user2_1.png",
        "user3_1.png",
        "user4_1.png",
    ]

    def __init__(
        self,
        group_name,
        connected_players,
        first_element_left_position,
        first_element_top_position,
        screen,
    ):
        self.group_name = group_name
        self.connected_players = connected_players
        self.first_element_left_position = first_element_left_position
        self.first_element_top_position = first_element_top_position
        self.screen = screen

        self.player_image_tiles = []
        self.player_name_tiles = []

    def add_player_tile(self, player_name):
        if len(self.player_image_tiles) >= self.MAX_PLAYERS_IN_GROUP:
            raise PlayerLimitExceededException()

        image_tile = Tile(
            f"player_{len(self.player_image_tiles) + 1}_image",
            common.get_image(self.player_images.pop(0)),
            self.screen,
            5,
            0,
            0
        )

        self.player_image_tiles.append(image_tile)

        surface = pygame.Surface([50, 12], pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        text_tile = PlainTextTile(
            f"player_{len(self.player_name_tiles) + 1}_text",
            surface,
            self.screen,
            22,
            0,
            0,
            player_name or "",
            40,
            15,
        )
        self.player_name_tiles.append(text_tile)

        self.center_player_tile(self.connected_players)

        self.connected_players += 1

    def resize_all_player_tiles(self):
        for i in range(0, self.connected_players):
            self.player_image_tiles[i].resize()
            self.player_name_tiles[i].resize()
            self.center_player_tile(i)

    def center_player_tile(self, index):
        image_left = self.first_element_left_position
        image_top = self.first_element_top_position
        if index > 0:
            image_left = self.player_image_tiles[index - 1].rect.left
            image_top = self.player_image_tiles[index - 1].rect.bottom + (self.screen.get_height() * 0.02)

        last_player_image_tile = self.player_image_tiles[index]

        last_player_image_tile.rect.left = image_left
        last_player_image_tile.rect.top = image_top

        text_left = last_player_image_tile.rect.right + (
            self.screen.get_width() * 0.007
        )
        text_centery = last_player_image_tile.rect.centery

        last_player_name_tile = self.player_name_tiles[index]

        last_player_name_tile.rect.left = text_left
        last_player_name_tile.rect.centery = text_centery

        # Center the text to the text box
        last_player_name_tile.center()

    def resize(self):
        self.resize_all_player_tiles()

    def blit(self):
        for i in range(0, self.connected_players):
            self.screen.blit(self.player_image_tiles[i].image, self.player_image_tiles[i].rect)
            self.screen.blit(self.player_name_tiles[i].image, self.player_name_tiles[i].rect)
            self.screen.blit(self.player_name_tiles[i].text_surface, self.player_name_tiles[i].text_rect)

    def clear_players(self):
        self.player_image_tiles = []
        self.player_name_tiles = []
        self.connected_players = 0

        self.player_images = [
            "user1_1.png",
            "user2_1.png",
            "user3_1.png",
            "user4_1.png",
        ]
