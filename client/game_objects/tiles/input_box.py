import pygame

import client
from client.utils import common


class InputBox:
    def __init__(self, screen, initial_text="", text_size=20):
        self.text = initial_text
        self.font = common.load_font(text_size)
        self.color = client.GAME_BASE_COLOR
        self.active = False
        self.text_surface = self.font.render(initial_text, True, client.GAME_BASE_COLOR)
        self.text_rect = self.text_surface.get_rect()
        self.screen = screen

    def mark_clicked(self):
        self.active = not self.active
        self.color = client.GAME_BASE_COLOR if self.active else client.NEUTRAL_COLOR

        if self.active:
            self.highlight(self.screen)

    def write(self, text):
        if self.active:
            self.text += text
            self.text_surface = self.font.render(self.text, True, self.color)
            self.text_rect = self.text_surface.get_rect()
            self.screen.blit(self.text_surface, self.text_rect)

    def delete(self):
        self.text = self.text[:-1]
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.screen.blit(self.text_surface, self.text_rect)

    def new_line(self):
        self.text = ""
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.screen.blit(self.text_surface, self.text_rect)

    def highlight(self, screen):
        # Draw the highlight.
        pygame.draw.rect(screen, self.color, self.text_rect, 10)
