import pygame
import client
import os
import uuid


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


def get_or_generate_player_id():
    # Open the player_id file or create it if not existing
    # and read the uuid or created if missing
    with open("player_id.txt", "a+") as f:
        if os.stat("player_id.txt").st_size == 0:
            f.write(str(uuid.uuid4()))
            f.write("\nUnknown")

    # Open the player_id file and read the uuid
    with open("player_id.txt", "r") as f:
        player_details = f.read()

    return player_details.split("\n")


def change_username(new_username):
    with open("player_id.txt", "r") as f:
        player_details = f.readlines()
        player_details = player_details[:-1]
        player_details.append(new_username)

    with open("player_id.txt", "w+") as f:
        f.writelines(player_details)


def get_image(image_name):
    if image_name not in client.IMAGE_CACHE:
        client.IMAGE_CACHE[image_name] = pygame.image.load(
            f"{client.IMG_PATH}{image_name}"
        ).convert_alpha()
    return client.IMAGE_CACHE[image_name]


def generate_transparent_image(width, height):
    transparent_image = pygame.Surface(
        [
            width,
            height,
        ],
        pygame.SRCALPHA,
        32,
    )
    transparent_image = transparent_image.convert_alpha()
    return transparent_image
