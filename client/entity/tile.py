import pygame.sprite
from pygame import sprite


class Tile(sprite.Sprite):
    def __init__(self, name, surface, screen, size_percent, tile_addition_width, tile_addition_height):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.image = surface

        self.screen = screen
        width, height = self.screen.get_size()
        self.standard_tile_width = width * size_percent

        self.standard_tile_height = (
            self.standard_tile_width * self.image.get_height() / self.image.get_width()
        )

        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.standard_tile_width) + tile_addition_width,
                int(self.standard_tile_height) + tile_addition_height,
            ),
        )

        self.rect = self.image.get_rect()

        self.screen.blit(self.image, self.rect)
