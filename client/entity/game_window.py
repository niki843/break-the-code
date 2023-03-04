from pygame.sprite import Group


class GameWindow:
    def __init__(self, screen):
        self.tiles_group = Group()

        self.screen = screen
        self.screen_rect = screen.get_rect()

    def blit(self):
        pass
