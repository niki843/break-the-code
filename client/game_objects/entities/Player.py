import client
from client.utils.enums import Position


class Player:
    def __init__(self, id, username, image_tile, text_bubble_tile, position: Position):
        self.id = id
        self.username = username
        self.image_tile = image_tile
        self.text_bubble_tile = text_bubble_tile
        self.position = position

    def position_image_tile(self):
        if self.position == Position.BOTTOM:
            self.image_tile.rect.bottom = client.state_manager.screen_rect.bottom - (
                client.state_manager.screen.get_height() * 0.01
            )
        elif self.position == Position.LEFT:
            pass
        elif self.position == Position.TOP:
            pass
        elif self.position == Position.RIGHT:
            pass

    def position_text_bubble(self):
        if self.position == Position.BOTTOM:
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top
            self.text_bubble_tile.rect.left = self. image_tile.rect.right
        elif self.position == Position.LEFT:
            self.text_bubble_tile.rect.left = self.image_tile.rect.right
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top
        elif self.position == Position.TOP:
            self.text_bubble_tile.rect.top = self.image_tile.rect.bottom
            self.text_bubble_tile.rect.left = self.image_tile.rect.right
        elif self.position == Position.RIGHT:
            self.text_bubble_tile.rect.right = self.image_tile.rect.left
            self.text_bubble_tile.rect.bottom = self.image_tile.rect.top