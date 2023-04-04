from client.game_objects.pages.game_window import GameWindow


class NewGame(GameWindow):
    def __init__(self, event_handler):
        super().__init__(event_handler)

        self.build()

    def build(self):
        self.build_new_game_background()

    def resize(self):
        super().resize()

    def open(self, **kwargs):
        super().open()
        self.event_handler.server_communication_manager.send_start_game_message()

    def blit(self):
        super().blit()
