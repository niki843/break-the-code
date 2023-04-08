import re

import client
from client.utils.enums import Position, AlignType


class Player:
    def __init__(self, id, username, image_tile, text_bubble_tile, cards, position: Position):
        self.id = id
        self.username = username
        self.image_tile = image_tile
        self.text_bubble_tile = text_bubble_tile
        self.cards = cards
        self.position = position

        self.position_tiles()

    def position_tiles(self):
        self.position_image_tile()
        self.position_text_bubble()
        self.position_cards()

    def position_image_tile(self):
        if self.position == Position.BOTTOM:
            self.image_tile.rect.bottom = client.state_manager.screen_rect.bottom - (
                    client.state_manager.screen.get_height() * 0.01
            )
            self.image_tile.rect.left = client.state_manager.screen_rect.left + (
                    client.state_manager.screen.get_width() * 0.3
            )
        elif self.position == Position.LEFT:
            self.image_tile.rect.left = client.state_manager.screen_rect.left + (
                    client.state_manager.screen.get_width() * 0.01
            )
            self.image_tile.rect.centery = client.state_manager.screen_rect.centery
        elif self.position == Position.TOP:
            self.image_tile.rect.top = client.state_manager.screen_rect.top + (
                    client.state_manager.screen.get_height() * 0.01
            )
            self.image_tile.rect.right = client.state_manager.screen_rect.right - (
                    client.state_manager.screen.get_width() * 0.3
            )
        elif self.position == Position.RIGHT:
            self.image_tile.rect.right = client.state_manager.screen_rect.right - (
                    client.state_manager.screen.get_width() * 0.01
            )
            self.image_tile.rect.centery = client.state_manager.screen_rect.centery

    def position_text_bubble(self):
        if self.position == Position.BOTTOM:
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top
            self.text_bubble_tile.rect.left = self.image_tile.rect.centerx
        elif self.position == Position.LEFT:
            self.text_bubble_tile.rect.left = self.image_tile.rect.centerx
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top
        elif self.position == Position.TOP:
            self.text_bubble_tile.rect.top = self.image_tile.rect.bottom
            self.text_bubble_tile.rect.right = self.image_tile.rect.centerx
        elif self.position == Position.RIGHT:
            self.text_bubble_tile.rect.right = self.image_tile.rect.centerx
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top

    def position_cards(self):
        if self.position == Position.BOTTOM:
            left = self.image_tile.rect.right
            for card in self.cards:
                card.rect.centery = self.image_tile.rect.centery
                card.rect.left = left + (
                        client.state_manager.screen.get_width() * 0.01
                )
                left = card.rect.right
        elif self.position == Position.LEFT:
            left = self.image_tile.rect.right + (
                    client.state_manager.screen.get_width() * 0.01
            )
            top = client.state_manager.screen_rect.top + (
                    client.state_manager.screen.get_height() * 0.3
            )
            for card in self.cards:
                card.rect.left = left
                card.rect.top = top

                left = card.rect.left
                top = card.rect.bottom + (
                        client.state_manager.screen.get_height() * 0.02
                )
        elif self.position == Position.TOP:
            right = self.image_tile.rect.left
            for card in self.cards:
                card.rect.centery = self.image_tile.rect.centery
                card.rect.right = right - (
                        client.state_manager.screen.get_width() * 0.01
                )
                right = card.rect.left
        elif self.position == Position.RIGHT:
            right = self.image_tile.rect.left - (
                    client.state_manager.screen.get_width() * 0.01
            )
            bottom = client.state_manager.screen_rect.bottom - (
                    client.state_manager.screen.get_height() * 0.3
            )
            for card in self.cards:
                card.rect.right = right
                card.rect.bottom = bottom

                right = card.rect.right
                bottom = card.rect.top - (
                        client.state_manager.screen.get_height() * 0.02
                )

    def give_condition_card_response(self, card, matching_cards, card_number_choice):
        if isinstance(matching_cards, list) and not matching_cards:
            if card.has_user_choice:
                text = card.negative_condition_message.format(card_number_choice)
            else:
                text = card.negative_condition_message
        elif card.has_user_choice:
            text = card.positive_condition_message.format(card_number_choice, matching_cards)
        elif matching_cards:
            text = card.positive_condition_message.format(matching_cards)
        else:
            text = card.negative_condition_message.format()

        text = re.sub("\[\|]", "", text)

        self.text_bubble_tile.replace_text(text)
        self.text_bubble_tile.center_text()
