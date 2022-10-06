import pygame


def check_events(background, screen):
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        return False
    elif event.type == pygame.VIDEORESIZE:
        screen.blit(pygame.transform.scale(background, event.dict['size']), (0, 0))
        pygame.display.flip()
