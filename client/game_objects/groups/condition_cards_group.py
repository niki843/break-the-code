import client
from client.game_objects.tiles.tile import Tile
from client.utils import common


class ConditionCardsGroup:
    def __init__(self, group_name, card_name, screen, condition_cards):
        self.condition_card_tiles = []
        self.group_name = group_name
        self.card_name = card_name
        self.screen = screen
        self.center_card = None
        self.load_center_card()
        self.load_new_condition_card_tiles(condition_cards)

    def load_center_card(self):
        self.center_card = Tile(
            f"{self.group_name}_center_card",
            common.get_image("card_back"),
            self.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
            0,
            0,
        )

    def center_center_card(self):
        self.center_card.rect.centerx = self.screen.get_rect().centerx
        self.center_card.rect.centery = self.screen.get_rect().centery

    def load_new_condition_card_tiles(self, condition_cards):
        self.condition_card_tiles = []
        for card in condition_cards:
            self.condition_card_tiles.append(
                Tile(
                    self.card_name,
                    common.get_image(f"card{card.id}.png"),
                    self.screen,
                    client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM,
                    0,
                    0,
                )
            )

    def center_condition_cards(self):
        # TODO Add centering cards according to the position of the center_card the should have relative
        #  to the screen size spacing
        pass

    def replace_card(self, old_card_tile, new_card_tile):
        self.condition_card_tiles[self.condition_card_tiles.index(old_card_tile)] = new_card_tile
        new_card_tile.rect.centerx = old_card_tile.rect.centerx
        new_card_tile.rect.centery = old_card_tile.rect.centery

    def remove_card(self, card_tile):
        self.condition_card_tiles[self.condition_card_tiles.index(card_tile)] = None

    def blit(self):
        self.screen.blit(self.center_card.image, self.center_card.rect)
        for card in self.condition_card_tiles:
            self.screen.blit(card.image, card.rect)

    def resize(self):
        self.center_card.resize()
        self.center_center_card()
        for condition_card in self.condition_card_tiles:
            condition_card.resize()
            self.center_condition_cards()
