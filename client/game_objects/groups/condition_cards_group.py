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
            common.get_image("card_back.png"),
            self.screen,
            17,
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
                    17,
                    0,
                    0,
                )
            )

    def center_condition_cards(self):
        self.condition_card_tiles[0].rect.centerx = self.center_card.rect.centerx
        self.condition_card_tiles[0].rect.bottom = self.center_card.rect.top - (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[1].rect.bottom = self.center_card.rect.centery
        self.condition_card_tiles[1].rect.left = self.center_card.rect.right + (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[2].rect.top = self.condition_card_tiles[1].rect.bottom + (
            self.screen.get_width() * 0.01
        )
        self.condition_card_tiles[2].rect.centerx = self.condition_card_tiles[1].rect.centerx

        self.condition_card_tiles[3].rect.centerx = self.center_card.rect.centerx
        self.condition_card_tiles[3].rect.top = self.center_card.rect.bottom + (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[4].rect.top = self.center_card.rect.centery + (
            self.screen.get_width() * 0.01
        )
        self.condition_card_tiles[4].rect.right = self.center_card.rect.left - (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[5].rect.bottom = self.condition_card_tiles[4].rect.top - (
            self.screen.get_width() * 0.01
        )
        self.condition_card_tiles[5].rect.centerx = self.condition_card_tiles[4].rect.centerx

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
