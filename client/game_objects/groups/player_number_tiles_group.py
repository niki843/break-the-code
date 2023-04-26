import time

import client

from client.game_objects.entities.player import Player
from client.game_objects.tiles.bubble_box_tile import BubbleBoxTile
from client.utils import common
from client.utils.enums import Position


class PlayerNumberTilesGroup:
    def __init__(self, group_name, tiles_name, player_id_name_map, number_cards=None):
        self.name = group_name
        self.tiles_name = tiles_name
        self.cards_amount = 4 if len(player_id_name_map) == 4 else 5

        self.number_cards = number_cards or []

        self.player_id_player_map = {}

        self.load_players(player_id_name_map)

    def load_players(self, player_id_name_map):
        all_positions = [Position.BOTTOM, Position.LEFT, Position.TOP, Position.RIGHT]
        size_by_position = {
            Position.BOTTOM: (21, 6.5),
            Position.LEFT: (21, 6.5),
            Position.TOP: (21, 6.5),
            Position.RIGHT: (21, 6.5),
        }

        index_of_current_player = list(player_id_name_map.keys()).index(
            client.state_manager.player_id
        )
        ordered_players = list(player_id_name_map.items())
        last_index = len(ordered_players) - 1

        for i in range(index_of_current_player - 1, -1, -1):
            player = ordered_players.pop(i)
            ordered_players.insert(last_index, player)

        for index, player_data in enumerate(ordered_players):
            position = all_positions[index]
            image_tile = common.load_tiny_tile(
                self.tiles_name,
                f"user{index+1}_w_background.png",
                client.state_manager.screen,
            )
            text_bubble = BubbleBoxTile(
                name="text_bubble",
                surface=common.get_image(f"result_bubble_{position}.png"),
                screen=client.state_manager.screen,
                size_percent=size_by_position[position][0],
                text_to_display="",
                text_size_percent=size_by_position[position][1],
            )

            cards = self.number_cards
            if index > 0:
                cards = self.load_card_backs(position)

            player = Player(
                player_data[0], player_data[1], image_tile, text_bubble, cards, position
            )
            self.player_id_player_map[player_data[0]] = player

    def load_card_backs(self, position):
        cards = []
        for i in range(0, self.cards_amount):
            if position == Position.LEFT:
                cards.append(
                    common.load_rotated_left_tile(
                        f"{chr(97 + i)}_card",
                        f"{chr(97 + i)}.png",
                        7,
                        client.state_manager.screen,
                    )
                )
                continue
            elif position == Position.RIGHT:
                cards.append(
                    common.load_rotated_right_tile(
                        f"{chr(97 + i)}_card",
                        f"{chr(97 + i)}.png",
                        7,
                        client.state_manager.screen,
                    )
                )
                continue
            elif position == Position.TOP:
                cards.append(
                    common.load_flipped_tile(
                        f"{chr(97 + i)}_card",
                        f"{chr(97 + i)}.png",
                        4.5,
                        client.state_manager.screen,
                    )
                )
        return cards

    def update_message(self, card, player_id, matching_cards, card_number_choice):
        player = self.player_id_player_map.get(player_id)

        response = player.give_condition_card_response(card, matching_cards, card_number_choice)

        return player.username, response

    def give_info_message(self, player_id, message):
        player = self.player_id_player_map.get(player_id)

        player.give_info_message(message)

    def resize(self):
        for player in self.player_id_player_map.values():
            player.image_tile.resize()
            player.text_bubble_tile.resize()
            player.username_text_tile.resize_text()
            for card in player.cards:
                card.resize()

    def center(self):
        for player in self.player_id_player_map.values():
            player.position_tiles()
            player.text_bubble_tile.center_text()

    def blit(self):
        for player in self.player_id_player_map.values():
            client.state_manager.screen.blit(
                player.image_tile.image, player.image_tile.rect
            )
            for card in player.cards:
                client.state_manager.screen.blit(card.image, card.rect)

            if (
                player.message_displayed_time
                and time.time() - player.message_displayed_time <= 5
            ):
                player.text_bubble_tile.blit()

            client.state_manager.screen.blit(
                player.username_text_tile.text_surface,
                player.username_text_tile.text_rect,
            )
