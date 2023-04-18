from client.game_objects.tiles.input_box_tile import InputBoxTile
from client.game_objects.tiles.toggle_tile import ToggleTile
from client.utils import common


class GuessCardTile(InputBoxTile):
    COLOR_BUTTONS = ["black", "white", "green"]
    COLOR_BUTTON_NAME = "color_button-{0}-guess_card-{1}"

    def __init__(
        self,
        guess_card_id,
        name,
        next_name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        initial_text="",
        text_size_percentage_from_screen_height=20,
        max_char=20,
    ):
        super().__init__(
            name,
            next_name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
            initial_text,
            text_size_percentage_from_screen_height,
            max_char,
        )

        self.guess_card_id = guess_card_id
        self.color_buttons = []
        self.clicked_color = None

        self.load_color_buttons()

    def load_color_buttons(self):
        for index, color in enumerate(self.COLOR_BUTTONS):
            color_button = ToggleTile(
                self.COLOR_BUTTON_NAME.format(index, self.guess_card_id),
                self.COLOR_BUTTON_NAME.format(index, self.guess_card_id),
                common.get_image(f"{color}_card_transparent.png"),
                self.screen,
                2,
                0,
                0,
                common.get_image(f"red-circle.png"),
            )
            setattr(color_button, "color", index)
            self.color_buttons.append(color_button)
            color_button.priority = 1

    def center_color_buttons(self):
        centerx = self.rect.centerx - self.image.get_width() * 0.25
        centery = self.rect.bottom - self.image.get_height() * 0.1
        for button in self.color_buttons:
            button.resize()
            button.rect.centerx = centerx
            button.rect.centery = centery

            centerx = centerx + self.image.get_width() * 0.25

    def mark_color(self, color_button_id):
        color_button = self.color_buttons[color_button_id]
        if (
            self.clicked_color
            and not self.clicked_color.name == f"color_button-{color_button_id}"
        ):
            self.clicked_color.next_value()
            self.clicked_color = None

        self.clicked_color = color_button if not self.clicked_color else None
        color_button.next_value()
