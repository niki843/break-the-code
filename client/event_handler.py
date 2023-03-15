import pygame
import json

from client import ws_client as client
from client.utils.singelton import Singleton


class EventHandler(Singleton):
    def __init__(self, player_id, current_window, screen):
        self.screen = screen
        self.current_window = current_window

        self.player_id = player_id

    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            return '{"type": "close_connection"}', True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                return self.handle_mouse_click()
            return None, False
        elif event.type == client.EVENT_TYPE:
            # TODO Implement when a server event happens
            print(event.message)
            return None, False
        elif (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and (
            keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]
        ):
            self.screen = pygame.display.set_mode(
                (0, 0), pygame.FULLSCREEN
            )
            self.current_window.change_screen(self.screen)
            self.current_window.delete()
            self.current_window.build()
            return None, False
        elif event.type == pygame.KEYUP and event.key == pygame.K_n:
            # TODO Remove this and all bellow when the game is complete
            return (
                f'{{"type": "new_game", "player_id": "{self.player_id}", "player_name": "first_player"}}',
                False,
            )
        elif event.type == pygame.KEYUP and event.key == pygame.K_c:
            return '{"type": "get_current_games"}', False
        elif event.type == pygame.KEYUP and event.key == pygame.K_j:
            game_session_id = input("game_session_id: ")
            return (
                f'{{"type": "join_game", "player_id": "{self.player_id}", "player_name": "second_player", "game_session_id": "{game_session_id}"}}',
                False,
            )
        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            return '{"type": "start_game"}', False
        elif event.type == pygame.KEYUP and event.key == pygame.K_p:
            condition_card_id = input("condition_card_id: ")
            return (
                f'{{"type": "play_tile", "condition_card_id": {condition_card_id}}}',
                False,
            )
        elif event.type == pygame.KEYUP and event.key == pygame.K_o:
            condition_card_id = input("condition_card_id: ")
            card_number_choice = input("card_number_choice: ")
            return (
                f'{{"type": "play_tile", "condition_card_id": {condition_card_id}, "card_number_choice": {card_number_choice}}}',
                False,
            )
        elif event.type == pygame and event.key == pygame.K_g:
            cards = []
            for i in range(0, 5):
                cards.append(input(f"{i} card"))
            return (
                f'{{"type": "guess_numbers", "player_guess": {json.dumps(cards)}}}',
                False,
            )
        else:
            return None, False

    def change_window(self, new_window):
        self.current_window = new_window

    def handle_mouse_click(self):
        print("Mouse is clicked")
        tiles_copy = self.current_window.tiles_group.copy()
        for tile in tiles_copy:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                print(tile.name)
                return self.current_window.activate_tile(tile, self)
        # Unclickable tile pressed
        return None, False
