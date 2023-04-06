import client

from copy import copy

from client.game_objects.entities.Player import Player
from client.utils import common
from client.utils.enums import Position


class PlayerNumberTilesGroup:
    def __init__(self, group_name, tiles_name, player_id_name_map, number_cards=None):
        self.name = group_name
        self.tiles_name = tiles_name
        self.is_four_player_game = True if len(player_id_name_map) == 4 else False
        self.cards_amount = 4 if self.is_four_player_game else 5

        self.user_icons = {}

        self.number_cards = number_cards or []
        self.left_letter_cards = []
        self.top_letter_cards = []
        self.bottom_letter_cards = []
        self.right_letter_cards = []

        self.player_id_text_bubble_map = {}
        self.player_id_player_map = {}

        self.load_user_icons(player_id_name_map)
        self.load_number_card_icons()

    def load_user_icons(self, player_id_name_map):
        all_positions = [Position.BOTTOM, Position.LEFT, Position.TOP, Position.RIGHT]

        index_of_current_player = list(player_id_name_map.keys()).index(client.state_manager.player_id)
        ordered_players = list(player_id_name_map)
        last_index = len(ordered_players) - 1

        for i in range(index_of_current_player - 1, -1, -1):
            player = ordered_players.pop(i)
            ordered_players.insert(last_index, player)

        for index, player_data in enumerate(ordered_players):
            image_tile = common.load_tiny_tile(self.tiles_name, f"user{index+1}_w_background.png", client.state_manager.screen)
            text_bubble = common.load_medium_tile("text_bubble", f"result_bubble_{all_positions[index]}.png", client.state_manager.screen)
            self.user_icons[all_positions[index]] = image_tile
            self.player_id_player_map[player_data[0]] = Player(player_data[0], player_data[1], image_tile, text_bubble, all_positions[index])

        self.position_user_icons()

    def position_user_icons(self):
        # Position bottom element
        self.user_icons.get(Position.BOTTOM).rect.bottom = client.state_manager.screen_rect.bottom - (
            client.state_manager.screen.get_height() * 0.01
        )
        self.user_icons.get(Position.BOTTOM).rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.3
        )

        # Position top element
        self.user_icons.get(Position.TOP).rect.top = client.state_manager.screen_rect.top + (
            client.state_manager.screen.get_height() * 0.01
        )
        self.user_icons.get(Position.TOP).rect.right = client.state_manager.screen_rect.right - (
            client.state_manager.screen.get_width() * 0.3
        )

        # Position left element
        self.user_icons.get(Position.LEFT).rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.01
        )
        self.user_icons.get(Position.LEFT).rect.centery = client.state_manager.screen_rect.centery

        if self.is_four_player_game:
            # Position right element
            self.user_icons.get(Position.RIGHT).rect.right = client.state_manager.screen_rect.right - (
                    client.state_manager.screen.get_width() * 0.01
            )
            self.user_icons.get(Position.RIGHT).rect.centery = client.state_manager.screen_rect.centery

    def load_number_card_icons(self):
        self.load_card_icons()

        self.position_number_card_icons()

    def load_card_icons(self):
        for i in range(0, self.cards_amount):
            card = common.load_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_top.png", client.state_manager.screen)
            self.top_letter_cards.append(copy(card))

            card_left = common.load_left_right_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_left.png", client.state_manager.screen)
            self.left_letter_cards.append(card_left)

            card_right = common.load_left_right_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_right.png", client.state_manager.screen)
            if self.is_four_player_game:
                self.right_letter_cards.append(card_right)

    def position_bottom_letter_cards(self):
        left = self.user_icons.get(Position.BOTTOM).rect.right
        for card in self.number_cards:
            card.rect.centery = self.user_icons.get(Position.BOTTOM).rect.centery
            card.rect.left = left + (
                client.state_manager.screen.get_width() * 0.01
            )
            left = card.rect.right

    def position_left_letter_cards(self):
        left = self.user_icons.get(Position.LEFT).rect.right + (
            client.state_manager.screen.get_width() * 0.01
        )
        top = client.state_manager.screen_rect.top + (
            client.state_manager.screen.get_height() * 0.3
        )
        for card in self.left_letter_cards:
            card.rect.left = left
            card.rect.top = top

            left = card.rect.left
            top = card.rect.bottom + (
                client.state_manager.screen.get_height() * 0.02
            )

    def position_top_letter_cards(self):
        right = self.user_icons.get(Position.TOP).rect.left
        for card in self.top_letter_cards:
            card.rect.centery = self.user_icons.get(Position.TOP).rect.centery
            card.rect.right = right - (
                client.state_manager.screen.get_width() * 0.01
            )
            right = card.rect.left

    def position_right_letter_cards(self):
        right = self.user_icons.get(Position.RIGHT).rect.left - (
            client.state_manager.screen.get_width() * 0.01
        )
        bottom = client.state_manager.screen_rect.bottom - (
            client.state_manager.screen.get_height() * 0.3
        )
        for card in self.right_letter_cards:
            card.rect.right = right
            card.rect.bottom = bottom

            right = card.rect.right
            bottom = card.rect.top - (
                client.state_manager.screen.get_height() * 0.02
            )

    def position_number_card_icons(self):
        self.position_bottom_letter_cards()
        self.position_left_letter_cards()
        self.position_top_letter_cards()
        if self.is_four_player_game:
            self.position_right_letter_cards()

    def resize(self):
        for tile in self.user_icons.values():
            tile.resize()

        for tile in self.bottom_letter_cards:
            tile.resize()
        for tile in self.left_letter_cards:
            tile.resize()
        for tile in self.top_letter_cards:
            tile.resize()
        if self.is_four_player_game:
            for tile in self.right_letter_cards:
                tile.resize()

    def center(self):
        self.position_user_icons()
        self.position_number_card_icons()

    def blit(self):
        # Blit user icons
        for tile in self.user_icons.values():
            client.state_manager.screen.blit(tile.image, tile.rect)

        # Blit shown number cards icons
        for number_tile in self.number_cards:
            client.state_manager.screen.blit(number_tile.image, number_tile.rect)

        for tile in self.left_letter_cards:
            client.state_manager.screen.blit(tile.image, tile.rect)
        for tile in self.top_letter_cards:
            client.state_manager.screen.blit(tile.image, tile.rect)
        if self.is_four_player_game:
            for tile in self.right_letter_cards:
                client.state_manager.screen.blit(tile.image, tile.rect)
