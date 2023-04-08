from client.game_objects.tiles.multiline_text_tile import MultilineTextTile
from client.utils.enums import AlignType


class BubbleBoxTile(MultilineTextTile):
    def __init__(
        self,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width,
        tile_addition_height,
        text_to_display: str,
        text_size_percent: float,
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width,
            tile_addition_height,
            text_to_display,
            text_size_percent,
            0,
        )

    def center_text(self, align_type=AlignType.CENTER):
        displayed_surfaces = self.text_surfaces[
            self.start_line: self.start_line + self.max_lines_to_display
        ]

        if len(displayed_surfaces) % 2 == 0:
            center_of_lower_element = self.rect.centery + (self.new_line_space/2) + (self.character_height/2)
            current_center = center_of_lower_element - (self.new_line_space + self.character_height * int(len(displayed_surfaces)/2))
        else:
            current_center = self.rect.centery - ((self.character_height + self.new_line_space) * int(len(displayed_surfaces)/2))

        for surface, rect in displayed_surfaces:
            if align_type == AlignType.LEFT:
                rect.left = self.rect.left + self.text_left_spacing
            elif align_type == AlignType.CENTER:
                rect.centerx = self.rect.centerx
            else:
                rect.right = self.rect.right + self.text_left_spacing
            rect.centery = current_center
            current_center = rect.bottom + self.new_line_space + (self.character_height/2)