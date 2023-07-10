import client
from client.utils import common


class NotesPopupGroup:
    def __init__(self, group_name, tiles_group):
        self.group_name = group_name
        self.tiles_group = tiles_group

        self.background = None

        self.player_notes_button = None

        self.is_open = False

        self.build()

    def build(self):
        self.build_background()
        self.build_notes_button()

    def resize(self):
        self.set_background_size()
        self.set_notes_button_size()

    def build_background(self):
        self.background = common.load_tile(
            "notes_background",
            common.get_image("notes_wo_side_win_cropped.png"),
            100,
            client.state_manager.screen,
        )
        self.background.priority = 2

        self.set_background_size()

    def set_background_size(self):
        if not self.background:
            return

        self.background.resize()
        self.background.rect.centerx = client.state_manager.screen_rect.centerx

        if self.is_open:
            self.background.rect.bottom = client.state_manager.screen_rect.bottom
        else:
            self.background.rect.top = client.state_manager.screen_rect.bottom

    def build_notes_button(self):
        self.player_notes_button = common.load_tile(
            "notes_arrow",
            common.get_image("notes_arrow.png"),
            10,
            client.state_manager.screen,
        )

        self.tiles_group.add(self.player_notes_button)
        self.set_notes_button_size()

    def set_notes_button_size(self):
        if not self.player_notes_button:
            return

        self.player_notes_button.resize()
        self.player_notes_button.rect.left = client.state_manager.screen_rect.left + (
            client.state_manager.screen.get_width() * 0.08
        )
        self.player_notes_button.rect.bottom = self.background.rect.top

    def clicked(self):
        self.close() if self.is_open else self.open()

    def open(self):
        self.is_open = True

        self.tiles_group.add(self.background)

        self.resize()

    def close(self):
        self.is_open = False

        self.tiles_group.remove(self.background)

        self.resize()

    def blit(self):
        client.state_manager.screen.blit(
            self.player_notes_button.image, self.player_notes_button.rect
        )

        if self.is_open:
            client.state_manager.screen.blit(
                self.background.image, self.background.rect
            )
