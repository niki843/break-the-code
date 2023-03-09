import pygame.image

from client import IMG_PATH, ARROW_WITH_PERCENTAGE_FROM_SCREEN
from client.entity.tile import Tile


class SlideshowTile(Tile):
    def __init__(self, name, surface, screen):
        super().__init__(name, surface, screen)

        self.right_arrow = pygame.image.load(f"{IMG_PATH}next.png").convert_alpha()

        self.standard_arrow_width = (
            self.screen.get_size()[0] * ARROW_WITH_PERCENTAGE_FROM_SCREEN
        )
        self.standard_arrow_height = (
            self.standard_arrow_width
            * self.right_arrow.get_height()
            / self.right_arrow.get_width()
        )

        self.right_arrow = pygame.transform.scale(self.right_arrow, (self.standard_arrow_width, self.standard_arrow_height))
        self.left_arrow = pygame.transform.flip(self.right_arrow, True, True)

        self.right_arrow_rect = self.right_arrow.get_rect()
        self.left_arrow_rect = self.left_arrow.get_rect()

    def update(self, *args, **kwargs) -> None:
        # self.right_arrow_rect.right = self.rect.right - self.right_arrow.get_width() - 5
        self.right_arrow_rect.centerx = 500
        self.right_arrow_rect.centery = 500

        self.left_arrow_rect.left = self.rect.left - self.left_arrow.get_width() + 5
        self.left_arrow_rect.centery = self.rect.centery

        self.screen.blit(self.right_arrow, self.right_arrow_rect)
        self.screen.blit(self.left_arrow, self.left_arrow_rect)
