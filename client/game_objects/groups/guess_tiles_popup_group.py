import client
from client.utils import common


class GuessTilesPopupGroup:
    def __init__(self, group_name):
        self.name = group_name

        self.is_open = False

        self.guess_button = None
        self.guess_popup_background = None

        self.build_guess_popup_background()

    def resize(self):
        self.set_guess_popup_background_size()

    def open(self, tiles_group):
        self.is_open = True
        tiles_group.add(self.guess_popup_background)

    def close(self, tiles_group):
        self.is_open = False
        tiles_group.remove(self.guess_popup_background)

    def build_guess_popup_background(self):
        self.guess_popup_background = common.load_tile(
            "guess_popup_backgound",
            common.get_image("menu_field_cropped.png"),
            40,
            client.state_manager.screen,
        )

        self.set_guess_popup_background_size()

    def set_guess_popup_background_size(self):
        if not self.guess_popup_background:
            return

        self.guess_popup_background.resize()
        self.guess_popup_background.rect.centerx = client.state_manager.screen_rect.centerx
        self.guess_popup_background.rect.centery = client.state_manager.screen_rect.centery

    def blit(self):
        if self.is_open:
            client.state_manager.screen.blit(self.guess_popup_background.image, self.guess_popup_background.rect)
