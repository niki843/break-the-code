from copy import copy

import pygame

from client.utils import common
from client.utils.enums import Position


class PlayerNumberTilesGroup:
    def __init__(self, group_name, tiles_name, screen, screen_rect, number_of_players, number_cards=None):
        self.screen = screen
        self.screen_rect = screen_rect
        self.name = group_name
        self.tiles_name = tiles_name
        self.is_four_player_game = True if number_of_players == 4 else False
        self.cards_amount = 4 if self.is_four_player_game else 5

        self.user_icons = {}

        self.number_cards = number_cards or []
        self.left_letter_cards = []
        self.top_letter_cards = []
        self.bottom_letter_cards = []
        self.right_letter_cards = []

        self.add_user_icons()
        self.load_number_card_icons()

    def add_user_icons(self):
        self.user_icons[Position.BOTTOM] = common.load_tiny_tile(self.tiles_name, "user1_w_background.png", self.screen)
        self.user_icons[Position.TOP] = common.load_tiny_tile(self.tiles_name, "user2_w_background.png", self.screen)
        self.user_icons[Position.LEFT] = common.load_tiny_tile(self.tiles_name, "user3_w_background.png", self.screen)

        if self.is_four_player_game:
            self.user_icons[Position.RIGHT] = common.load_tiny_tile(self.tiles_name, "user4_w_background.png", self.screen)

        self.position_user_icons()

    def position_user_icons(self):
        # Position bottom element
        self.user_icons.get(Position.BOTTOM).rect.bottom = self.screen_rect.bottom - (
            self.screen.get_height() * 0.01
        )
        self.user_icons.get(Position.BOTTOM).rect.left = self.screen_rect.left + (
            self.screen.get_width() * 0.3
        )

        # Position top element
        self.user_icons.get(Position.TOP).rect.top = self.screen_rect.top + (
            self.screen.get_height() * 0.01
        )
        self.user_icons.get(Position.TOP).rect.right = self.screen_rect.right - (
            self.screen.get_width() * 0.3
        )

        # Position left element
        self.user_icons.get(Position.LEFT).rect.left = self.screen_rect.left + (
            self.screen.get_width() * 0.01
        )
        self.user_icons.get(Position.LEFT).rect.centery = self.screen_rect.centery

        if self.is_four_player_game:
            # Position right element
            self.user_icons.get(Position.RIGHT).rect.right = self.screen_rect.right - (
                    self.screen.get_width() * 0.01
            )
            self.user_icons.get(Position.RIGHT).rect.centery = self.screen_rect.centery

    def load_number_card_icons(self):
        self.load_card_icons()

        self.position_number_card_icons()

    def load_card_icons(self):
        for i in range(0, self.cards_amount):
            card = common.load_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_top.png", self.screen)
            self.top_letter_cards.append(copy(card))

            card_left = common.load_left_right_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_left.png", self.screen)
            self.left_letter_cards.append(card_left)

            card_right = common.load_left_right_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_right.png", self.screen)
            if self.is_four_player_game:
                self.right_letter_cards.append(card_right)

    def position_bottom_letter_cards(self):
        left = self.user_icons.get(Position.BOTTOM).rect.right
        for card in self.number_cards:
            card.rect.centery = self.user_icons.get(Position.BOTTOM).rect.centery
            card.rect.left = left + (
                self.screen.get_width() * 0.01
            )
            left = card.rect.right

    def position_left_letter_cards(self):
        left = self.user_icons.get(Position.LEFT).rect.right + (
            self.screen.get_width() * 0.01
        )
        top = self.screen_rect.top + (
            self.screen.get_height() * 0.3
        )
        for card in self.left_letter_cards:
            card.rect.left = left
            card.rect.top = top

            left = card.rect.left
            top = card.rect.bottom + (
                self.screen.get_height() * 0.02
            )

    def position_top_letter_cards(self):
        right = self.user_icons.get(Position.TOP).rect.left
        for card in self.top_letter_cards:
            card.rect.centery = self.user_icons.get(Position.TOP).rect.centery
            card.rect.right = right - (
                self.screen.get_width() * 0.01
            )
            right = card.rect.left

    def position_right_letter_cards(self):
        right = self.user_icons.get(Position.RIGHT).rect.left - (
            self.screen.get_width() * 0.01
        )
        bottom = self.screen_rect.bottom - (
            self.screen.get_height() * 0.3
        )
        for card in self.right_letter_cards:
            card.rect.right = right
            card.rect.bottom = bottom

            right = card.rect.right
            bottom = card.rect.top - (
                self.screen.get_height() * 0.02
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
            self.screen.blit(tile.image, tile.rect)

        # Blit shown number cards icons
        for number_tile in self.number_cards:
            self.screen.blit(number_tile.image, number_tile.rect)

        for tile in self.left_letter_cards:
            self.screen.blit(tile.image, tile.rect)
        for tile in self.top_letter_cards:
            self.screen.blit(tile.image, tile.rect)
        if self.is_four_player_game:
            for tile in self.right_letter_cards:
                self.screen.blit(tile.image, tile.rect)
