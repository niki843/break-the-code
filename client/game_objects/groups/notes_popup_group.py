import client
from client.utils import common


class NotesPopupGroup:
    GUESS_NUMBER_BLACK_TILES_NAME = "{0}_black_tile"
    GUESS_NUMBER_WHITE_TILES_NAME = "{0}_white_tile"

    def __init__(self, group_name, tiles_group):
        self.group_name = group_name
        self.tiles_group = tiles_group

        self.guess_number_tiles = []

        self.background = None
        self.next_background = None

        self.player_notes_button = None

        self.is_open = False

        self.build()

    def build(self):
        self.build_background()
        self.build_notes_button()
        self.build_guess_numbers_tiles()

    def resize(self):
        self.set_background_size()
        self.set_notes_button_size()
        self.set_guess_numbers_tile_size()

    def build_background(self):
        self.background = common.load_tile(
            "notes_background",
            common.get_image("notes_wo_side_win_cropped.png"),
            100,
            client.state_manager.screen,
        )
        self.next_background = common.load_tile(
            "notes_background",
            common.get_image("notes_w_side_win_cropped.png"),
            69.8,
            client.state_manager.screen,
        )
        self.background.priority = 2
        self.next_background.priority = 2

        self.set_background_size()
        self.set_background_size()

    def set_background_size(self):
        if not self.background:
            return

        self.background.resize()
        self.background.rect.left = client.state_manager.screen_rect.left

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

    def build_guess_numbers_tiles(self):
        x_distance_percentage = 3.5
        y_distance_percentage = 5
        for i in range(0, 10):
            tile1 = common.load_movable_tile(
                        self.background,
                        x_distance_percentage,
                        y_distance_percentage,
                        self.GUESS_NUMBER_BLACK_TILES_NAME.format(i),
                        common.get_image(f"{i}.png"),
                        3.2,
                        client.state_manager.screen
            )
            tile2 = common.load_movable_tile(
                        self.background,
                        x_distance_percentage,
                        y_distance_percentage,
                        self.GUESS_NUMBER_WHITE_TILES_NAME.format(i),
                        common.get_image(f"{i}.png"),
                        3.2,
                        client.state_manager.screen
            )
            self.tiles_group.add(tile1)
            self.tiles_group.add(tile2)
            tile1.priority = 3
            tile2.priority = 3
            self.guess_number_tiles.append((tile1, tile2))

            x_distance_percentage = x_distance_percentage + 3.5

        self.set_guess_numbers_tile_size()

    def set_guess_numbers_tile_size(self):
        if not self.guess_number_tiles:
            return

        for tile1, tile2 in self.guess_number_tiles:
            tile1.resize()
            tile2.resize()

            tile1.rect.left, tile1.rect.top = tile1.get_position()
            tile2.rect.left, tile2.rect.top = tile2.get_position()

    def clicked(self):
        self.close() if self.is_open else self.open()

    def open(self):
        self.is_open = True

        self.tiles_group.add(self.background)
        self.tiles_group.remove(self.next_background)

        self.resize()

    def close(self):
        self.is_open = False

        self.tiles_group.remove(self.background)
        self.tiles_group.remove(self.next_background)

        self.resize()

    def scale(self):
        temp = self.background
        self.background = self.next_background
        self.next_background = temp

        for tile1, tile2 in self.guess_number_tiles:
            tile1.change_reference_object(self.background)
            tile2.change_reference_object(self.background)

        self.set_guess_numbers_tile_size()

        self.resize()

    def blit(self):
        client.state_manager.screen.blit(
            self.player_notes_button.image, self.player_notes_button.rect
        )

        if self.is_open:
            client.state_manager.screen.blit(
                self.background.image, self.background.rect
            )

            for tile1, tile2 in self.guess_number_tiles:
                client.state_manager.screen.blit(
                    tile1.image, tile1.rect
                )
                client.state_manager.screen.blit(
                    tile2.image, tile2.rect
                )
