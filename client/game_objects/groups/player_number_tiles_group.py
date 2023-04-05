from client.utils import common
from client.utils.enums import Position


class PlayerNumberTilesGroup:
    def __init__(self, group_name, tiles_name, screen, screen_rect, number_of_players, number_cards=None):
        self.number_cards = number_cards
        self.screen = screen
        self.screen_rect = screen_rect
        self.name = group_name
        self.tiles_name = tiles_name
        self.number_of_players = number_of_players

        self.user_icons = {}

        self.add_user_icons()

    def add_user_icons(self):
        self.user_icons[Position.BOTTOM] = common.load_tiny_tile(self.tiles_name, "user1_w_background.png", self.screen)
        self.user_icons[Position.TOP] = common.load_tiny_tile(self.tiles_name, "user2_w_background.png", self.screen)
        self.user_icons[Position.LEFT] = common.load_tiny_tile(self.tiles_name, "user3_w_background.png", self.screen)

        if self.number_of_players == 4:
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

        if self.number_of_players == 4:
            # Position right element
            self.user_icons.get(Position.RIGHT).rect.right = self.screen_rect.right - (
                    self.screen.get_width() * 0.01
            )
            self.user_icons.get(Position.RIGHT).rect.centery = self.screen_rect.centery

    def resize(self):
        for tile in self.user_icons.values():
            tile.resize()

    def center(self):
        self.position_user_icons()

    def blit(self):
        for tile in self.user_icons.values():
            self.screen.blit(tile.image, tile.rect)
