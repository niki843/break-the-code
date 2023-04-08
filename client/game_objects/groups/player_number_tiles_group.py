import client

from client.game_objects.entities.player import Player
from client.game_objects.tiles.bubble_box_tile import BubbleBoxTile
from client.utils import common
from client.utils.enums import Position


class PlayerNumberTilesGroup:
    def __init__(self, group_name, tiles_name, player_id_name_map, number_cards=None):
        self.name = group_name
        self.tiles_name = tiles_name
        self.is_four_player_game = True if len(player_id_name_map) == 4 else False
        self.cards_amount = 4 if self.is_four_player_game else 5

        self.number_cards = number_cards or []
        self.left_letter_cards = []
        self.top_letter_cards = []
        self.bottom_letter_cards = []
        self.right_letter_cards = []

        self.player_id_text_bubble_map = {}
        self.player_id_player_map = {}

        self.load_players(player_id_name_map)
        # self.load_number_card_icons()

    def load_players(self, player_id_name_map):
        all_positions = [Position.BOTTOM, Position.LEFT, Position.TOP, Position.RIGHT]
        size_by_position = {Position.BOTTOM: (21, 6.5), Position.LEFT: (21, 6.5), Position.TOP: (21, 6.5), Position.RIGHT: (21, 6.5)}

        index_of_current_player = list(player_id_name_map.keys()).index(client.state_manager.player_id)
        ordered_players = list(player_id_name_map.items())
        last_index = len(ordered_players) - 1

        for i in range(index_of_current_player - 1, -1, -1):
            player = ordered_players.pop(i)
            ordered_players.insert(last_index, player)

        for index, player_data in enumerate(ordered_players):
            position = all_positions[index]
            image_tile = common.load_tiny_tile(self.tiles_name, f"user{index+1}_w_background.png", client.state_manager.screen)
            text_bubble = BubbleBoxTile(
                "text_bubble",
                common.get_image(f"result_bubble_{position}.png"),
                client.state_manager.screen,
                size_by_position[position][0],
                0,
                0,
                "",
                size_by_position[position][1],
            )

            cards = self.number_cards
            if index > 0:
                cards = self.load_card_backs(position)

            player = Player(player_data[0], player_data[1], image_tile, text_bubble, cards, position)
            self.player_id_player_map[player_data[0]] = player

    def load_card_backs(self, position):
        cards = []
        for i in range(0, self.cards_amount):
            if position == Position.LEFT or position == Position.RIGHT:
                cards.append(common.load_left_right_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_{position}.png", client.state_manager.screen))
                continue
            cards.append(common.load_number_tile(f"{chr(97 + i)}_card", f"{chr(97 + i)}_{position}.png", client.state_manager.screen))
        return cards

    def update_message(self, card, player_id, matching_cards, card_number_choice):
        player = self.player_id_player_map.get(player_id)

        player.give_condition_card_response(card, matching_cards, card_number_choice)

    def resize(self):
        for player in self.player_id_player_map.values():
            player.image_tile.resize()
            player.text_bubble_tile.resize()
            for card in player.cards:
                card.resize()

    def center(self):
        for player in self.player_id_player_map.values():
            player.position_tiles()

    def blit(self):
        for player in self.player_id_player_map.values():
            client.state_manager.screen.blit(player.image_tile.image, player.image_tile.rect)
            for card in player.cards:
                client.state_manager.screen.blit(card.image, card.rect)
            player.text_bubble_tile.blit()
