from client.game_objects.tiles.tile import Tile


class ToggleTile(Tile):
    def __init__(
        self,
        name,
        next_name,
        current_surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        next_surface,
        shrink_percent=0,
    ):
        super().__init__(
            name,
            current_surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.next_surface = Tile(
            next_name,
            next_surface,
            screen,
            size_percent - shrink_percent,
            tile_addition_width,
            tile_addition_height,
        )

        self.values = (self, self.next_surface)

    def next_value(self):
        self.next_surface.rect.centerx = self.rect.centerx
        self.next_surface.rect.centery = self.rect.centery

        temp_image = self.image
        temp_original_image = self.original_image
        temp_rect = self.rect
        temp_name = self.name

        self.image = self.next_surface.image
        self.original_image = self.next_surface.original_image
        self.name = self.next_surface.name

        self.rect = self.next_surface.rect

        self.next_surface.image = temp_image
        self.next_surface.original_image = temp_original_image
        self.next_surface.rect = temp_rect
        self.next_surface.name = temp_name

    def resize(self):
        super().resize()
        if hasattr(self, "next_surface"):
            self.next_surface.resize()
