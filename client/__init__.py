import os
import asyncio

IMG_PATH = f".{os.path.sep}resources{os.path.sep}images{os.path.sep}"
FONT_PATH = f".{os.path.sep}resources{os.path.sep}fonts{os.path.sep}"
MUSIC_PATH = f".{os.path.sep}resources{os.path.sep}music{os.path.sep}"

TILE_WIDTH_ADDITION_PERCENT = 3.9
TILE_HEIGHT_ADDITION_PERCENT = 0

BETWEEN_TILES_SPACING = 10

BETWEEN_TILE_AND_SCREEN_SPACING = 20

TILE_WIDTH_PERCENTAGE_FROM_SCREEN_TINY = 7
TILE_WIDTH_PERCENTAGE_FROM_SCREEN_VERY_SMALL = 9
TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMALL = 12
TILE_WIDTH_PERCENTAGE_FROM_SCREEN_SMEDIUM = 14
TILE_WIDTH_PERCENTAGE_FROM_SCREEN_MEDIUM = 18
TILE_WIDTH_PERCENTAGE_FROM_SCREEN_BIG = 36

ARROW_WITH_PERCENTAGE_FROM_SCREEN = 5
TEXT_SIZE_PERCENTAGE_FROM_BOX = 10

ASYNC_SLEEP_TIME_ON_EXIT = 0.5

GAME_BASE_COLOR = (0, 0, 1)
NEUTRAL_COLOR = (0, 0, 0)
OLD_GAME_BASE_COLOR = (127, 169, 6)

LOOP = asyncio.get_event_loop()

IS_FULLSCREEN_ENABLED = False

LEFT_BUTTON_CLICK = 1
SCROLL_UP = 4
SCROLL_DOWN = 5

IMAGE_CACHE = {}

state_manager = None
server_communication_manager = None

DEFAULT_RESOLUTION_STR = "1280x720"
DEFAULT_RESOLUTION_TUPLE = (1280, 720)

DEFAULT_MUSIC = "main_music.mp3"
DEFAULT_THUMBNAIL = "logo_thumbnail.png"

GAME_NAME = "Break The Code"

# IMPORTANT!!! This is how the game will know if the game should stop running
GAME_RUNNING = True

# Game constants shared between the server and client
MISSING_PROPERTY_DEFAULT = -1
CARD_INDEX_TO_LETTER_MAP = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}
