import client
from client.game_objects.tiles.guess_card_tile import GuessCardTile
from client.utils import common
from client.utils.enums import GameTypes


class GuessTilesPopupGroup:
    GUESS_CARD_NAME = "guess_card-{0}"
    SUBMIT_BUTTON_NAME = "guess_popup_submit_button"

    def __init__(self, group_name):
        self.name = group_name

        self.is_open = False

        self.guess_popup_background = None
        self.guess_cards = []

        self.submit_button = None

    def resize(self):
        self.set_guess_popup_background_size()
        self.set_guess_cards_size()
        self.set_submit_button_size()

    def open(self, tiles_group):
        if not self.guess_cards:
            self.build_guess_popup_background()
            self.build_guess_cards()
            self.build_submit_button()
        self.is_open = True
        tiles_group.add(self.guess_popup_background)
        tiles_group.add(self.submit_button)
        for card in self.guess_cards:
            tiles_group.add(card)
            for color_button in card.color_buttons:
                tiles_group.add(color_button)

    def close(self, tiles_group):
        self.is_open = False
        tiles_group.remove(self.guess_popup_background)
        tiles_group.remove(self.submit_button)
        for card in self.guess_cards:
            tiles_group.remove(card)
            for color_button in card.color_buttons:
                tiles_group.remove(color_button)

    def build_guess_popup_background(self):
        self.guess_popup_background = common.load_tile(
            self.SUBMIT_BUTTON_NAME,
            common.get_image("menu_field_cropped.png"),
            50 if client.state_manager.game_type == GameTypes.THREE_PLAYER else 40,
            client.state_manager.screen,
        )

        self.set_guess_popup_background_size()

    def set_guess_popup_background_size(self):
        if not self.guess_popup_background:
            return

        self.guess_popup_background.resize()
        self.guess_popup_background.rect.centerx = (
            client.state_manager.screen_rect.centerx
        )
        self.guess_popup_background.rect.centery = (
            client.state_manager.screen_rect.centery
        )

    def build_guess_cards(self):
        cards_amm = 5 if client.state_manager.game_type == GameTypes.THREE_PLAYER else 4

        for i in range(0, cards_amm):
            self.guess_cards.append(
                GuessCardTile(
                    i,
                    self.GUESS_CARD_NAME.format({i}),
                    self.GUESS_CARD_NAME.format({i}),
                    common.get_image("user_number_1.png"),
                    client.state_manager.screen,
                    8,
                    0,
                    0,
                    common.get_image("user_number_pressed.png"),
                    text_size_percentage_from_screen_height=5,
                    max_char=1,
                )
            )

        self.set_guess_cards_size()

    def set_guess_cards_size(self):
        if not self.guess_cards:
            return

        left = self.guess_popup_background.rect.left + (
            client.state_manager.screen.get_width() * 0.017
        )
        centery = self.guess_popup_background.rect.centery
        for card in self.guess_cards:
            card.resize()
            card.rect.left = left
            card.rect.centery = centery

            left = card.rect.right + (client.state_manager.screen.get_width() * 0.017)
            card.center_color_buttons()

    def build_submit_button(self):
        self.submit_button = common.load_tile(
            "guess_popup_submit_button",
            common.get_image("submit.png"),
            12,
            client.state_manager.screen,
        )

        self.set_submit_button_size()

    def set_submit_button_size(self):
        if not self.submit_button:
            return

        self.submit_button.resize()
        self.submit_button.rect.centerx = client.state_manager.screen_rect.centerx
        self.submit_button.rect.bottom = self.guess_popup_background.rect.bottom + (
            client.state_manager.screen.get_height() * 0.05
        )

    def mark_color(self, tile_name):
        guess_card_id, color_button_id = self.__get_color_button_id_and_card_id(
            tile_name
        )

        self.guess_cards[guess_card_id].mark_color(color_button_id)

    def get_guess(self):
        cards = []
        for card in self.guess_cards:
            if not card.clicked_color or not card.text:
                return
            cards.append(f"{card.clicked_color.color}{card.text}")
        return '["' + '", "'.join(cards) + '"]'

    def blit(self):
        if self.is_open:
            client.state_manager.screen.blit(
                self.guess_popup_background.image, self.guess_popup_background.rect
            )

            for guess_card in self.guess_cards:
                guess_card.blit()
                for color_button in guess_card.color_buttons:
                    client.state_manager.screen.blit(
                        color_button.image, color_button.rect
                    )

            client.state_manager.screen.blit(
                self.submit_button.image, self.submit_button.rect
            )

    @staticmethod
    def __get_color_button_id_and_card_id(tile_name):
        all_elements = tile_name.split("-")
        color_button_id = int(all_elements[1])
        guess_card_id = int(all_elements[3])

        return guess_card_id, color_button_id
