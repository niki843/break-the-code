# A file used to store common functions used throughout the game
import pygame
import client


def get_percentage_multiplier_from_percentage(percentage: float):
    return percentage / 100


def load_font(width):
    return pygame.font.Font(
        f"{client.FONT_PATH}SilkRemington-SBold.ttf",
        int(width),
    )


def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()
