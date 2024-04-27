import client

from game_objects.tiles.tile import Tile


class MovableTile(Tile):
    """
    A class representing a movable tile image.
    Inheriting Tile class and all it's attributes.
    ...

    Attributes
    ----------
    reference_object : Tile
        Object that will be use as reference point when the object is moved to keep track of the position
                !!!!THE STARTING POINT IS TOP-LEFT OF THE REFERENCE OBJECT!!!!
    x_distance_percentage : float
        Distance from the left of the reference object in percent
    y_distance_percentage : float
        Distance from the top of the reference object in percent
    name : str
        the name that will be used to reference the image tile
    surface : pygame.Surface
        the surface that will be displayed as a tile and used to show text on top
    screen : pygame.Surface
        the main surface on which the game is being displayed
    size_percent : str
        percent representation of what the size of the image compared to the surface would be
    tile_addition_width_percent : int
        used for addition to the width of the image that's being used, uses percent of the screen width
    tile_addition_height_percent : int
        used for addition to the height of the image that's being used, uses percent of the screen height
    """
    def __init__(
        self,
        reference_object,
        x_distance_percentage,
        y_distance_percentage,
        name,
        surface,
        screen,
        size_percent,
        tile_addition_width_percent=0,
        tile_addition_height_percent=0
    ):
        super().__init__(
            name,
            surface,
            screen,
            size_percent,
            tile_addition_width_percent,
            tile_addition_height_percent,
        )

        self.reference_object = reference_object
        self.x_distance_percentage = x_distance_percentage
        self.y_distance_percentage = y_distance_percentage

    def get_position(self):
        x_position = self.reference_object.rect.left + (client.state_manager.screen.get_width() * (self.x_distance_percentage / 100))
        y_position = self.reference_object.rect.top + (client.state_manager.screen.get_height() * (self.y_distance_percentage / 100))

        return x_position, y_position

    def change_reference_object(self, reference_object: Tile):
        self.reference_object = reference_object

    def move_slider(self, event):
        # TODO implement this
        x_movement, y_movement = event.pos
