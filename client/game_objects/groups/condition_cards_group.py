import numpy
import time

import client
from client.game_objects.tiles.tile import Tile
from client.utils import common
from client.game_objects.tiles.toggle_tile import ToggleTile


class ConditionCardsGroup:
    def __init__(self, group_name, card_name, screen, condition_cards):
        self.condition_card_tiles = []
        self.condition_card_id_tile_map = {}
        self.group_name = group_name
        self.card_name = card_name
        self.screen = screen
        self.center_card = None
        self.load_center_card()
        self.load_new_condition_card_tiles(condition_cards)

        self.transparent_background = None
        self.maximized_choice_tile = None
        self.first_choice_tile = None
        self.second_choice_tile = None

        self.old_tile = None
        self.old_tile_displayed_time = None
        self.old_tile_number_choice_tile = None

    def load_center_card(self):
        self.center_card = Tile(
            f"{self.group_name}_center_card",
            common.get_image("card_back.png"),
            self.screen,
            17,
        )

    def center_center_card(self):
        """Center the card that's in the center"""
        self.center_card.rect.centerx = self.screen.get_rect().centerx
        self.center_card.rect.centery = self.screen.get_rect().centery

    def load_new_condition_card_tiles(self, condition_cards):
        self.condition_card_tiles = []
        self.condition_card_id_tile_map = {}
        for card in condition_cards:
            tile = Tile(
                f"{self.card_name}-{card.id}",
                common.get_image(f"card{card.id}.png"),
                self.screen,
                17,
            )
            self.condition_card_tiles.append(tile)
            self.condition_card_id_tile_map[str(card.id)] = tile

    def center_condition_cards(self):
        self.condition_card_tiles[0].rect.centerx = self.center_card.rect.centerx
        self.condition_card_tiles[0].rect.bottom = self.center_card.rect.top - (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[1].rect.bottom = self.center_card.rect.centery
        self.condition_card_tiles[1].rect.left = self.center_card.rect.right + (
            self.screen.get_width() * 0.01
        )

        self.condition_card_tiles[2].rect.top = self.condition_card_tiles[
            1
        ].rect.bottom + (self.screen.get_width() * 0.01)
        self.condition_card_tiles[2].rect.centerx = self.condition_card_tiles[
            1
        ].rect.centerx

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

        self.condition_card_tiles[5].rect.bottom = self.condition_card_tiles[
            4
        ].rect.top - (self.screen.get_width() * 0.01)
        self.condition_card_tiles[5].rect.centerx = self.condition_card_tiles[
            4
        ].rect.centerx

    def replace_card(self, old_card_tile, new_card_tile, tiles_group, card_number_choice=None):
        self.old_tile = old_card_tile
        self.remove_card_choice_popup(tiles_group)
        self.replace_card_with_placeholder(old_card_tile, new_card_tile)
        new_card_tile.rect.centerx = old_card_tile.rect.centerx
        new_card_tile.rect.centery = old_card_tile.rect.centery

        if card_number_choice:
            self.old_tile_number_choice_tile = Tile(
                name=f"{card_number_choice}-first_choice_tile_off",
                surface=common.get_image(f"choice_{card_number_choice}.png"),
                screen=self.screen,
                size_percent=7,
            )
            self.old_tile_number_choice_tile.priority = 3

        self.maximize_old_tile()

    def replace_card_with_placeholder(self, old_card_tile, new_card_tile):
        self.condition_card_id_tile_map[self.get_card_id(new_card_tile)] = new_card_tile
        self.condition_card_tiles[
            self.condition_card_tiles.index(old_card_tile)
        ] = new_card_tile

    def remove_card_choice_popup(self, tiles_group):
        if self.maximized_choice_tile:
            tiles_group.remove([
                self.first_choice_tile,
                self.second_choice_tile,
                self.transparent_background
            ])
            self.old_tile = self.maximized_choice_tile

            self.first_choice_tile = None
            self.second_choice_tile = None
            self.maximized_choice_tile = None
            self.transparent_background = None

    def open_condition_number_choice(self, card):
        self.first_choice_tile = ToggleTile(
            name=f"{card.choices[0]}-first_choice_tile_off",
            next_name=f"{card.choices[0]}-first_choice_tile_on",
            current_surface=common.get_image(f"choice_{card.choices[0]}.png"),
            screen=self.screen,
            size_percent=7,
            next_surface=common.get_image(f"choice_{card.choices[0]}_active.png"),
            shrink_percent=0,
            is_on=False
        )
        self.first_choice_tile.priority = 3

        self.second_choice_tile = ToggleTile(
            name=f"{card.choices[1]}-second_choice_tile_off",
            next_name=f"{card.choices[1]}-second_choice_tile_on",
            current_surface=common.get_image(f"choice_{card.choices[1]}.png"),
            screen=self.screen,
            size_percent=7,
            next_surface=common.get_image(f"choice_{card.choices[1]}_active.png"),
            shrink_percent=0,
            is_on=False
        )
        self.second_choice_tile.priority = 3

        self.transparent_background = Tile(
            f"choice_card_transparent_bgr",
            common.generate_transparent_image(self.screen.get_width(), self.screen.get_height()),
            self.screen,
            100,
        )
        self.transparent_background.priority = 2
        card_tile = self.get_tile_by_id(str(card.id))

        placeholder_tile = Tile(
            f"condition_card_placeholder-{card.id}",
            common.generate_transparent_image(card_tile.image.get_width(), card_tile.image.get_height()),
            self.screen,
            17,
        )
        placeholder_tile.rect.centerx = card_tile.rect.centerx
        placeholder_tile.rect.centery = card_tile.rect.centery
        self.replace_card_with_placeholder(card_tile, placeholder_tile)

        self.maximized_choice_tile = card_tile
        self.maximize_choice_card(card_tile)

    def maximize_choice_card(self, card_tile):
        self.old_tile = card_tile
        self.old_tile.size_percent = 30
        self.resize_old_tile()
        self.old_tile = None

        self.first_choice_tile.rect.centery = card_tile.rect.bottom
        self.first_choice_tile.rect.right = card_tile.rect.centerx - (self.screen.get_width() * 0.01)
        self.second_choice_tile.rect.centery = card_tile.rect.bottom
        self.second_choice_tile.rect.left = card_tile.rect.centerx + (self.screen.get_width() * 0.01)

    def maximize_old_tile(self):
        self.old_tile.size_percent = 30
        self.resize_old_tile()

        self.old_tile_displayed_time = time.time()

    def resize_old_tile(self):
        self.old_tile.resize()
        self.old_tile.rect.centerx = client.state_manager.screen_rect.centerx
        self.old_tile.rect.centery = client.state_manager.screen_rect.centery

        if self.old_tile_number_choice_tile:
            self.old_tile_number_choice_tile.resize()
            self.old_tile_number_choice_tile.rect.centerx = self.old_tile.rect.centerx
            self.old_tile_number_choice_tile.rect.centery = self.old_tile.rect.bottom

    def remove_card(self, card_tile):
        self.condition_card_tiles.pop(self.condition_card_tiles.index(card_tile))
        self.condition_card_id_tile_map.pop(self.get_card_id(card_tile))

    def missing_card(self, card_ids):
        missing = numpy.setdiff1d(self.condition_card_id_tile_map.keys(), card_ids)
        if len(missing) > 1:
            raise Exception("too many missing cards")
        return missing[0]

    def get_card_id(self, card_tile):
        return card_tile.name.split("-")[1]

    def get_tile_by_id(self, card_id: str):
        return self.condition_card_id_tile_map.get(card_id)

    def blit(self):
        self.screen.blit(self.center_card.image, self.center_card.rect)
        for card in self.condition_card_tiles:
            self.screen.blit(card.image, card.rect)

        if self.maximized_choice_tile:
            self.screen.blit(self.maximized_choice_tile.image, self.maximized_choice_tile.rect)
        if self.first_choice_tile:
            self.screen.blit(self.first_choice_tile.image, self.first_choice_tile.rect)
            self.screen.blit(self.second_choice_tile.image, self.second_choice_tile.rect)
        if self.transparent_background:
            self.screen.blit(self.transparent_background.image, self.transparent_background.rect)

        if self.old_tile and time.time() - self.old_tile_displayed_time <= 5:
            self.screen.blit(self.old_tile.image, self.old_tile.rect)
            if self.old_tile_number_choice_tile:
                self.screen.blit(self.old_tile_number_choice_tile.image, self.old_tile_number_choice_tile.rect)
        elif self.old_tile and self.old_tile.rect.left <= client.state_manager.screen_rect.right:
            self.old_tile.rect.left += self.screen.get_width() * 0.009
            self.screen.blit(self.old_tile.image, self.old_tile.rect)
            if self.old_tile_number_choice_tile:
                self.old_tile_number_choice_tile.rect.left += self.screen.get_width() * 0.009
                self.screen.blit(self.old_tile_number_choice_tile.image, self.old_tile_number_choice_tile.rect)
        elif self.old_tile:
            self.old_tile = None
            self.old_tile_number_choice_tile = None

    def resize(self):
        self.center_card.resize()
        self.center_center_card()
        if self.old_tile:
            self.resize_old_tile()
        for condition_card in self.condition_card_tiles:
            condition_card.resize()
            self.center_condition_cards()
