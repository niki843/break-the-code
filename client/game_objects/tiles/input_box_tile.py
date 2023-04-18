import client
from client.game_objects.tiles.input_box import InputBox
from client.game_objects.tiles.toggle_tile import ToggleTile


class InputBoxTile(ToggleTile, InputBox):
    def __init__(
        self,
        name,
        next_name,
        surface,
        screen,
        size_percent,
        next_surface,
        initial_text="",
        text_size_percentage_from_screen_height=20,
        max_char=20,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0,
    ):
        ToggleTile.__init__(
            self,
            name,
            next_name,
            surface,
            screen,
            size_percent,
            next_surface,
            tile_addition_width_percent=tile_addition_width_percent,
            tile_addition_height_percent=tile_addition_height_percent,
        )
        InputBox.__init__(
            self,
            initial_text,
            text_size_percentage_from_screen_height,
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

    def resize(self):
        super().resize()
        if hasattr(self, "text_rect"):
            self.resize_text()

    def blit(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)
