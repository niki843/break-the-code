import time

import pygame
import json

from client import ws_client as client, LOOP
from client.game_objects.pages.join_game import JoinGame
from client.game_objects.pages.menu import Menu
from client.game_objects.pages.new_game import NewGame
from client.game_objects.pages.settings import Settings
from client.utils import common
from client.utils.singelton import Singleton


class EventHandler(Singleton):
    def __init__(self, player_id, screen):
        self.game_windows = []
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.current_window = Menu(self)

        self.player_id = player_id

        self.menu = self.current_window
        self.settings = Settings(self)
        self.new_game = NewGame(self)
        self.join_game = JoinGame(self)

        self.game_windows.append(self.menu)
        self.game_windows.append(self.settings)
        self.game_windows.append(self.new_game)
        self.game_windows.append(self.join_game)

    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            return '{"type": "close_connection"}', True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.handle_mouse_click()
        elif event.type == client.EVENT_TYPE:
            # TODO Implement when a server event happens
            self.handle_server_message(event.message)
            print(event.message)
        elif (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and (
            keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]
        ):
            self.open_full_screen()
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
        return None, False

    # 15/03/2023 NT: An interesting implementation here it turns out that in order to write and not affect anything else
    # we need to enter another infinite while to wait for text input and exit it on click.
    # Another interesting thing here, this causes a type of circular recursion
    # between handle_mouse_click, activate_tile, and wait_text_input which is kind of necessary to be able to
    # click on another tile while writing.
    # 16/03/2023 NT: We need to copy the main game code for async tasks run and display rendering and so on
    # in order to be able to execute other events while still waiting for user input in text box. This will allow us
    # to have a different button binding while not in writing mode, where in writing mode it won't be possible.
    def wait_text_input(self, text_surface):
        writing = True
        while writing:
            events = pygame.event.get()
            pygame.display.flip()
            for event in events:
                keys = pygame.key.get_pressed()
                if event.type == client.EVENT_TYPE:
                    # TODO Implement when a server event happens
                    self.handle_server_message(event.message)
                    print(event.message)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        text_surface.new_line()
                    elif event.key == pygame.K_BACKSPACE:
                        text_surface.delete()
                    else:
                        text_surface.write(event.unicode)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        text_surface.mark_clicked()
                        return self.handle_mouse_click()
                elif event.type == pygame.QUIT:
                    return '{"type": "close_connection"}', True
                elif (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and (
                        keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]
                ):
                    self.open_full_screen()

            text_surface.center()
            self.current_window.blit()

            common.run_once(LOOP)

        return None, False

    def handle_slider_clicked(self, slider):
        clicked = True
        while clicked:
            events = pygame.event.get()
            pygame.display.flip()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False
                if event.type == pygame.MOUSEMOTION:
                    slider.move_slider(event.pos[0])
            self.current_window.blit()

    def handle_save_button(self, button):
        mouse_clicked = True
        while mouse_clicked:
            events = pygame.event.get()
            pygame.display.flip()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    button.next_value()
                    mouse_clicked = False
            self.current_window.blit()

    def change_window(self, new_window):
        self.current_window = new_window

    def change_screen(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        for window in self.game_windows:
            window.resize()

    def handle_mouse_click(self):
        print("Mouse is clicked")
        tiles_copy = self.current_window.tiles_group.copy()
        for tile in tiles_copy:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                print(tile.name)
                return self.current_window.activate_tile(tile)
        # Unclickable tile pressed
        return None, False

    def handle_server_message(self, message):
        pass

    def open_full_screen(self):
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )
        self.change_screen(self.screen)
        self.settings.resolution_slider.handle_position = self.settings.SCREEN_SIZE_CAPTIONS.index("fullscreen")
        return None, False
