from client.game_objects.tiles.tile import Tile


class ToggleTile(Tile):

    def __init__(
            self,
            name,
            current_surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            next_surface,
    ):
        super().__init__(
            name,
            current_surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.next_surface = Tile("music_toggle_on", next_surface, screen, size_percent, tile_addition_width, tile_addition_height)

        self.values = (self, self.next_surface)

    def next_value(self):
        self.next_surface.rect.centerx = self.rect.centerx
        self.next_surface.rect.centery = self.rect.centery

        temp_image = self.image
        temp_rect = self.rect

        index = self.values.index(self) - 1
        self.image = self.values[index].image

        self.rect = self.next_surface.rect

        self.next_surface.image = temp_image
        self.next_surface.rect = temp_rect

