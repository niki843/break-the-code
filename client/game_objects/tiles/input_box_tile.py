import client
from client.game_objects.tiles.input_box import InputBox
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common


class InputBoxTile(ToggleTile, InputBox):
    def __init__(
        self,
        name,
        next_name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        initial_text="",
        text_size_percentage=20,
        max_char=20,
    ):
        ToggleTile.__init__(
            self,
            name,
            next_name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface
        )
        InputBox.__init__(
            self,
            screen,
            initial_text,
            int(self.image.get_height() * common.get_percentage_multiplier_from_percentage(text_size_percentage)),
            max_char,
        )

    def mark_clicked(self):
        self.active = not self.active
        self.color = client.GAME_BASE_COLOR if self.active else client.NEUTRAL_COLOR
        self.draw()

    def draw(self):
        self.next_value()

    def center(self):
        self.text_rect.centerx = self.rect.centerx
        self.text_rect.centery = self.rect.centery
