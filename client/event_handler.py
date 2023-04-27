import pygame
import client as client_init

from client import ws_client as client, LOOP
from client.game_objects.pages.join_game import JoinGame
from client.game_objects.pages.lobby import Lobby
from client.game_objects.pages.menu import Menu
from client.game_objects.pages.new_game import NewGame
from client.game_objects.pages.settings import Settings
from client.utils import common
from client.utils.singelton import Singleton


REQUEST_TYPE_WINDOW_FUNCTION_MAP = {
    "send_game_sessions": "update_game_sessions",
    "player_joined": "add_player",
    "game_created": "add_game_session_id",
    "host_disconnected": "replace_host",
    "player_removed": "remove_player",
    "start_game": "start_game",
    "give_condition_cards": "load_condition_cards",
    "give_number_cards": "load_number_cards",
    "card_condition_result": "replace_card_and_give_result",
    "player_eliminated": "show_player_eliminated",
    "end_game": "show_player_won",
    "end_game_no_winners": "show_end_game_no_winners",
    "player_disconnected": "set_player_disconnected",
    "game_session_closed": "remove_game_session"
}


class EventHandler(Singleton):
    def __init__(self):
        self.game_windows = []
        self.current_window = Menu(self)

        self.menu = self.current_window
        self.settings = Settings(self)
        self.new_game = NewGame(self)
        self.join_game = JoinGame(self)
        self.lobby = Lobby(self)

        self.game_windows.append(self.menu)
        self.game_windows.append(self.settings)
        self.game_windows.append(self.new_game)
        self.game_windows.append(self.join_game)
        self.game_windows.append(self.lobby)

    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        self.check_common_events(event, keys)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)

    # 15/03/2023 NT: An interesting implementation here it turns out that in order to write and not affect anything else
    # we need to enter another infinite while to wait for text input and exit it on click next click.
    # 16/03/2023 NT: We need to copy the main game code for async tasks run and display rendering and so on
    # in order to be able to execute other events while still waiting for user input in text box. This will allow us
    # to have a different button binding while not in writing mode, where in writing mode it won't be possible.
    def wait_text_input(self, text_surface):
        waiting_text_input = True
        while waiting_text_input:
            events = pygame.event.get()
            pygame.display.flip()
            for event in events:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LALT] or keys[pygame.K_RALT]:
                    text_surface.mark_clicked()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if text_surface.active:
                        text_surface.mark_clicked()
                    # !!!! Recursion !!!
                    # Doesn't break anything though tested it with about 50 levels
                    self.handle_mouse_click(event)
                    return

                waiting_text_input = self.check_common_events(event, keys)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        text_surface.mark_clicked()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text_surface.delete()
                    else:
                        text_surface.write(event.unicode)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    text_surface.mark_clicked()
                    self.handle_mouse_click(event)
                    return

            text_surface.center()
            self.current_window.blit()
            self.current_window.position_and_blit_cursor()

            common.run_once(LOOP)

    def check_common_events(self, event, keys):
        if event.type == pygame.QUIT:
            self.current_window.close()
            client_init.server_communication_manager.close_connection()
            client_init.GAME_RUNNING = False
            # Returning False for is_game_running
            return False
        elif event.type == client.EVENT_TYPE:
            self.handle_server_message(event.message)
        elif (
            (keys[pygame.K_LALT] or keys[pygame.K_RALT])
            and (keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN])
            and event.type == pygame.KEYDOWN
        ):
            if not client_init.IS_FULLSCREEN_ENABLED:
                self.open_full_screen()
            elif client_init.IS_FULLSCREEN_ENABLED:
                self.open_windowed_screen()
        return True

    def handle_slider_clicked(self, slider):
        clicked = True
        while clicked:
            events = pygame.event.get()
            pygame.display.flip()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False
                if event.type == pygame.MOUSEMOTION:
                    slider.move_slider(event)
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
            self.current_window.position_and_blit_cursor()

    def change_window(self, new_window):
        self.current_window = new_window

    def change_screen(self, screen):
        client_init.state_manager.screen = screen
        client_init.state_manager.screen_rect = screen.get_rect()

        for window in self.game_windows:
            window.resize()

    def handle_mouse_click(self, event):
        tiles_copy = self.current_window.tiles_group.copy()
        clicked_sprites = tiles_copy.get_sprites_at(pygame.mouse.get_pos())
        if tiles_copy.get_sprites_at(pygame.mouse.get_pos()):
            # !!!! Important if two sprites have the same priority and are overlapping this will return
            # the on that was added second from both !!!!!!!!!!!!!
            clicked_tiles_priority = {tile.priority: tile for tile in clicked_sprites}
            max_priority_tile = clicked_tiles_priority.get(
                max(clicked_tiles_priority.keys())
            )
            print(f"Maximum priority tile: {max_priority_tile.name}")
            return self.current_window.activate_tile(max_priority_tile, event)

    def handle_server_message(self, message):
        message_type = message.get("type")

        if message_type == "player_joined":
            if client_init.state_manager.player_id == message.get("player_id"):
                return

        window_function = REQUEST_TYPE_WINDOW_FUNCTION_MAP.get(message_type)
        if window_function:
            getattr(self.current_window, window_function)(**message)

    def open_full_screen(self):
        screen = pygame.display.set_mode((1366, 768), pygame.HWSURFACE)
        self.change_screen(screen)
        self.settings.resolution_slider.handle_position = len(self.settings.SCREEN_SIZE_CAPTIONS) - 1
        self.settings.resolution_slider.set_slider_handle_position()
        self.join_game.reset_selected_game_session()
        client_init.IS_FULLSCREEN_ENABLED = True

    def open_windowed_screen(self):
        screen = pygame.display.set_mode(
            client_init.DEFAULT_RESOLUTION_TUPLE, pygame.HWSURFACE
        )
        self.change_screen(screen)
        self.settings.resolution_slider.handle_position = (
            self.settings.SCREEN_SIZE_CAPTIONS.index(client_init.DEFAULT_RESOLUTION_STR)
        )
        self.settings.resolution_slider.set_slider_handle_position()
        self.join_game.reset_selected_game_session()
        client_init.IS_FULLSCREEN_ENABLED = False
