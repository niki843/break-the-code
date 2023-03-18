import pygame

import client
from client.utils import common


class InputBox:
    def __init__(self, screen, initial_text="", text_size_percentage_from_screen_height=20, max_char=20):
        self.text = initial_text
        self.text_size_percentage = text_size_percentage_from_screen_height
        self.color = client.GAME_BASE_COLOR
        self.active = False
        self.font = None
        self.text_surface = None
        self.text_rect = None
        self.screen = screen
        self.max_char = max_char

        self.resize_text()

    def mark_clicked(self):
        self.active = not self.active
        self.color = client.GAME_BASE_COLOR if self.active else client.NEUTRAL_COLOR

        if self.active:
            self.highlight()

    def write(self, text):
        if len(self.text) < self.max_char:
            self.text += text
            self.text_surface = self.font.render(self.text, True, self.color)
            self.text_rect = self.text_surface.get_rect()

    def delete(self):
        self.text = self.text[:-1]
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()

    def new_line(self):
        self.text = ""
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()

    def highlight(self):
        # Draw the highlight.
        pygame.draw.rect(self.screen, self.color, self.text_rect, 10)

    def resize_text(self):
        text_size = int(self.screen.get_height() * common.get_percentage_multiplier_from_percentage(self.text_size_percentage))
        self.font = common.load_font(text_size)
        self.text_surface = self.font.render(self.text, True, client.GAME_BASE_COLOR)
        self.text_rect = self.text_surface.get_rect()
        # self.screen.blit(self.text_surface, self.text_rect)
