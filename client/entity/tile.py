import pygame.sprite
from pygame import sprite

TILE_WIDTH_ADDITION = 50
TILE_HEIGHT_ADDITION = 0


class Tile(sprite.Sprite):
    def __init__(self, surface, screen):
        pygame.sprite.Sprite.__init__(self)

        self.image = surface

        self.screen = screen
        width, height = self.screen.get_size()
        self.standard_tile_width = width * 0.18

        self.standard_tile_height = (
            self.standard_tile_width
            * self.image.get_height()
            / self.image.get_width()
        )

        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.standard_tile_width) + TILE_WIDTH_ADDITION,
                int(self.standard_tile_height) + TILE_HEIGHT_ADDITION,
            ),
        )

        self.rect = self.image.get_rect()

        self.screen.blit(self.image, self.rect)
