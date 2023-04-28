import client

from client.game_objects.cards.card_reader import CardReader
from client.custom_exceptions.no_such_card_exception import (
    NoSuchCardException,
)
from client.game_objects.groups.condition_cards_group import ConditionCardsGroup
from client.game_objects.groups.guess_tiles_popup_group import GuessTilesPopupGroup
from client.game_objects.groups.played_cards_popup_group import PlayedCardsPopupGroup
from client.game_objects.groups.player_number_tiles_group import PlayerNumberTilesGroup
from client.game_objects.pages.game_window import GameWindow
from client.game_objects.tiles.input_box import InputBox
from client.game_objects.tiles.tile import Tile
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common
from client.utils.enums import Colors, GameTypes


class NewGame(GameWindow):
    CONDITION_CARD_NAME = "condition_card-{0}"

    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.non_played_condition_cards = {}
        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        self.number_cards = []

        self.condition_cards_group = None
        self.player_number_tiles_group = None
        self.guess_tiles_popup_group = None

        self.guess_button = None
        self.end_game_message = None
        self.back_to_menu_button = None

        self.player_notes_button = None
        self.player_notes = None

        self.played_cards_group = None

        self.player_on_hand_id = None

        self.eliminated_player_ids = []

        self.build()

    def build(self):
        self.build_new_game_background()
        self.tiles_group.add(self.background_image)

        self.build_guess_tile()
        self.build_notes_button()

        self.build_played_cards_popup()

    def resize(self):
        super().resize()

        self.set_condition_cards_size()

        self.set_player_number_group_size()

        self.set_guess_tile_size()

        self.set_guess_tiles_group_size()

        self.set_end_game_message_size()
        self.set_back_to_menu_size()

        self.set_notes_button_size()

        self.set_played_cards_popup_size()

    def build_draw_pile(self, condition_cards):
        self.condition_cards_group = ConditionCardsGroup(
            "condition_cards_group",
            "condition_card",
            client.state_manager.screen,
            condition_cards,
        )

        self.set_condition_cards_size()

    def set_condition_cards_size(self):
        if not self.condition_cards_group:
            return

        self.condition_cards_group.resize()

    def load_number_cards(self, cards, **kwargs):
        self.number_cards = []
        for card in cards:
            self.number_cards.append(
                Tile(
                    "number_card",
                    common.get_image(
                        f"{card.get('number')}_{Colors(card.get('color'))}.png"
                    ),
                    client.state_manager.screen,
                    5,
                )
            )
        self.build_player_number_group()

    def build_player_number_group(self):
        self.player_number_tiles_group = PlayerNumberTilesGroup(
            "player_number_group",
            "number_card",
            self.player_info_group.get_player_name_id_map(),
            self.number_cards,
        )

        self.set_player_number_group_size()

    def set_player_number_group_size(self):
        if not self.player_number_tiles_group:
            return

        self.player_number_tiles_group.resize()
        self.player_number_tiles_group.center()

    def build_guess_tile(self):
        surface = common.get_image("guess.png")
        self.guess_button = common.load_tile(
            "guess_button",
            surface,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            client.state_manager.screen
        )

        self.tiles_group.add(self.guess_button)
        self.set_guess_tile_size()

    def set_guess_tile_size(self):
        if not self.guess_button:
            return

        self.guess_button.resize()
        self.guess_button.rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.05
        )
        self.guess_button.rect.top = client.state_manager.screen_rect.top + (
            client.state_manager.screen.get_height() * 0.05
        )

    def load_condition_cards(self, condition_card_ids, **kwargs):
        if self.current_drawn_condition_cards or self.played_condition_cards:
            return

        for card_id in condition_card_ids:
            if card_id in self.current_drawn_condition_cards:
                continue
            card = self.non_played_condition_cards.pop(int(card_id))
            self.current_drawn_condition_cards[card_id] = card

        self.build_draw_pile(self.current_drawn_condition_cards.values())
        self.tiles_group.add(self.condition_cards_group.condition_card_tiles)

    def replace_card_and_give_result(
        self, card_id, next_card_id, player_results, card_number_choice=None, **kwargs
    ):
        played_card = self.remove_played_card(card_id)

        player_name_responses_map = {}
        for result in player_results:
            player_name, player_response = self.player_number_tiles_group.update_message(
                played_card,
                result.get("player_id"),
                result.get("matching_cards"),
                card_number_choice,
            )
            player_name_responses_map[player_name] = player_response

        if not next_card_id:
            self.condition_cards_group.remove_card(
                self.condition_cards_group.get_tile_by_id(str(card_id))
            )
            return

        self.draw_condition_card(next_card_id)

        new_card = Tile(
            self.CONDITION_CARD_NAME.format(next_card_id),
            common.get_image(f"card{next_card_id}.png"),
            client.state_manager.screen,
            17,
        )
        old_card = self.condition_cards_group.get_tile_by_id(str(card_id))

        self.condition_cards_group.replace_card(old_card, new_card)

        self.tiles_group.add(new_card)

        self.played_cards_group.add_played_card(old_card.copy(), player_name_responses_map)

        self.next_player()

    def draw_condition_card(self, card_id):
        card = self.non_played_condition_cards.pop(card_id)

        if not card:
            raise NoSuchCardException(card_id, "or is already drawn")

        self.current_drawn_condition_cards[card.id] = card

    def remove_played_card(self, card_id):
        card = self.current_drawn_condition_cards.pop(card_id)

        if not card:
            raise NoSuchCardException(card_id, "or is already played or not drawn yet")

        self.played_condition_cards[card_id] = card

        card_tile = self.condition_cards_group.get_tile_by_id(card_id)
        self.tiles_group.remove(card_tile)

        return card

    def build_guess_popup(self):
        self.guess_tiles_popup_group = GuessTilesPopupGroup("guess_tiles_group")

    def set_guess_tiles_group_size(self):
        if not self.guess_tiles_popup_group:
            return

        self.guess_tiles_popup_group.resize()

    def build_end_game_message(self, size, message):
        self.end_game_message = InputBox(
            message,
            size,
            40
        )

        self.set_end_game_message_size()

    def set_end_game_message_size(self):
        if not self.end_game_message:
            return

        self.end_game_message.resize_text()
        self.end_game_message.text_rect.centerx = client.state_manager.screen_rect.centerx
        self.end_game_message.text_rect.centery = client.state_manager.screen_rect.centery

    def build_back_to_menu_button(self):
        self.back_to_menu_button = ToggleTile(
            "back_to_menu_button",
            "back_to_menu_button",
            common.get_image("back.png"),
            client.state_manager.screen,
            client.TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL,
            common.get_image("back_pressed.png"),
            shrink_percent=1,
        )

        self.tiles_group.add(self.back_to_menu_button)
        self.set_back_to_menu_size()

    def set_back_to_menu_size(self):
        if not self.back_to_menu_button:
            return

        self.back_to_menu_button.resize()
        self.back_to_menu_button.rect.top = self.end_game_message.text_rect.bottom + (
            client.state_manager.screen.get_height() * 0.01
        )
        self.back_to_menu_button.rect.centerx = client.state_manager.screen_rect.centerx

    def build_notes_button(self):
        self.player_notes_button = common.load_tile("notes_arrow", common.get_image("notes_arrow.png"), 10, client.state_manager.screen)

        self.tiles_group.add(self.player_notes_button)
        self.set_notes_button_size()

    def set_notes_button_size(self):
        if not self.player_notes_button:
            return

        self.player_notes_button.resize()
        self.player_notes_button.rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.08
        )
        self.player_notes_button.rect.bottom = client.state_manager.screen_rect.bottom

    def build_played_cards_popup(self):
        self.played_cards_group = PlayedCardsPopupGroup("played_cards", self.tiles_group)

    def set_played_cards_popup_size(self):
        if not self.played_cards_group:
            pass

        self.played_cards_group.resize()

    def show_player_eliminated(self, player_id, **kwargs):
        if player_id == client.state_manager.player_id:
            client.state_manager.is_player_eliminated = True

        self.player_number_tiles_group.give_info_message(player_id, "I've tried to guess the cards incorrectly")
        self.next_player()
        self.remove_player(player_id)

        # This if should really always be True but just wanted to make sure
        if player_id not in self.eliminated_player_ids:
            print(f"Eliminating player {player_id}")
            self.eliminated_player_ids.append(player_id)

    def show_player_won(self, winner_id, message, **kwargs):
        self.player_number_tiles_group.give_info_message(winner_id, "I've guessed the cards correctly")
        if winner_id == client.state_manager.player_id:
            self.build_end_game_message(20, "You won!")
            self.build_back_to_menu_button()
            client.state_manager.is_player_eliminated = True
        else:
            self.build_end_game_message(10, message)
            self.build_back_to_menu_button()

    def show_end_game_no_winners(self, **kwargs):
        self.build_end_game_message(10, "All players eliminated, no winners!")
        self.build_back_to_menu_button()
        client.state_manager.is_player_eliminated = True

    def remove_player(self, player_id, **kwargs):
        if self.player_on_hand_id == player_id:
            self.next_player()
        id_name_map = self.player_info_group.get_player_name_id_map()
        self.player_info_group.remove_player(id_name_map.get(player_id))

    def add_player(self, player_id, player_name, **kwargs):
        if player_id not in self.eliminated_player_ids:
            print(f"Adding player {player_id}")
            self.player_info_group.add_player_tile(player_id, player_name)

    def next_player(self):
        next_player_id = self.player_info_group.player_ids.index(self.player_on_hand_id) + 1 - len(self.player_info_group.player_ids)
        self.player_on_hand_id = self.player_info_group.player_ids[next_player_id]

    def set_player_disconnected(self, player_id, **kwargs):
        print(f"Player disconnected {player_id}")

    def can_player_use_server_actions(self):
        if (
                client.state_manager.is_player_eliminated
                or client.state_manager.player_id != self.player_on_hand_id
        ):
            return False
        if self.condition_cards_group.old_tile:
            return False
        return True

    def open(self, **kwargs):
        super().open()
        client.server_communication_manager.send_start_game_message()
        cr = CardReader()

        self.player_info_group = kwargs.get("player_info_group")

        self.player_on_hand_id = self.player_info_group.player_ids[0]

        client.state_manager.game_type = GameTypes.FOUR_PLAYER if self.player_info_group.connected_players == 4 else GameTypes.THREE_PLAYER

        self.build_guess_popup()

        for card in cr.cards:
            self.non_played_condition_cards[card.id] = card

    def close(self):
        super().close()
        client.state_manager.is_player_eliminated = False
        self.tiles_group.remove(self.back_to_menu_button)

        self.end_game_message = None
        self.back_to_menu_button = None

        self.non_played_condition_cards.update(self.played_condition_cards)
        self.non_played_condition_cards.update(self.current_drawn_condition_cards)

        self.played_condition_cards = {}
        self.current_drawn_condition_cards = {}

        client.server_communication_manager.send_exit_game_message()

    def activate_tile(self, tile, event):
        match event.button:
            case client.LEFT_BUTTON_CLICK:
                self.tile_left_button_click_event(tile)
            case client.SCROLL_UP:
                pass
            case client.SCROLL_DOWN:
                pass

    def tile_left_button_click_event(self, tile):
        match tile.name:
            case name if name.startswith(self.CONDITION_CARD_NAME.format("")):
                if not self.can_player_use_server_actions():
                    return

                card_id = self.condition_cards_group.get_card_id(tile)
                card = self.current_drawn_condition_cards.get(int(card_id))

                if card.has_user_choice:
                    client.server_communication_manager.play_choice_condition_card(
                        card.id, card.choices[0]
                    )
                    return

                client.server_communication_manager.play_condition_card(card.id)

                if self.guess_tiles_popup_group.is_open:
                    self.guess_tiles_popup_group.close(self.tiles_group)
            case self.guess_button.name:
                if self.guess_tiles_popup_group.is_open:
                    self.guess_tiles_popup_group.close(self.tiles_group)
                self.guess_tiles_popup_group.open(self.tiles_group)
            case self.background_image.name:
                self.guess_tiles_popup_group.close(self.tiles_group)
            case name if name.startswith(self.guess_tiles_popup_group.GUESS_CARD_NAME.format("")):
                tile.mark_clicked()
                self.event_handler.wait_text_input(tile)
            case name if name.startswith("color_button"):
                self.guess_tiles_popup_group.mark_color(name)
            case GuessTilesPopupGroup.SUBMIT_BUTTON_NAME:
                cards_guess = self.guess_tiles_popup_group.get_guess()
                if not cards_guess:
                    return
                client.server_communication_manager.guess_cards(cards_guess)
                self.guess_tiles_popup_group.close(self.tiles_group)
            case self.played_cards_group.played_cards_button.name:
                self.played_cards_group.clicked()

        if self.back_to_menu_button and self.back_to_menu_button.name == tile.name:
            self.close()
            self.event_handler.menu.open()

    def blit(self):
        super().blit()

        if self.condition_cards_group:
            self.condition_cards_group.blit()

        if self.player_number_tiles_group:
            self.player_number_tiles_group.blit()

        if self.end_game_message:
            client.state_manager.screen.blit(self.end_game_message.text_surface, self.end_game_message.text_rect)

        if self.back_to_menu_button:
            client.state_manager.screen.blit(self.back_to_menu_button.image, self.back_to_menu_button.rect)

        client.state_manager.screen.blit(self.guess_button.image, self.guess_button.rect)

        self.guess_tiles_popup_group.blit()

        client.state_manager.screen.blit(self.player_notes_button.image, self.player_notes_button.rect)

        self.played_cards_group.blit()
