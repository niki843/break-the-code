MISSING_PROPERTY_DEFAULT = -1
NUMBER_CARDS_PER_PLAYER_TWO_OR_THREE_PLAYERS = 5
NUMBER_CARDS_PER_PLAYER_FOUR_PLAYERS = 4
NUMBER_CARDS_COUNT = 20
CARD_INDEX_TO_LETTER_MAP = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}

CARDS_REQUIRING_USER_INPUT_MAP = {
    1: [8, 9],
    16: [1, 2],
    21: [3, 4]
}

ERROR_MESSAGE_TYPE = "error"
GAME_CREATED_MESSAGE_TYPE = "game_created"
PLAYER_JOINED_MESSAGE_TYPE = "player_joined"
PLAYER_ELIMINATED_MESSAGE_TYPE = "player_eliminated"
INCORRECT_INPUT_MESSAGE_TYPE = "incorrect_input"
CONNECTION_CLOSED_MESSAGE_TYPE = "connection_closed"

ERROR_TYPE_INSUFFICIENT_PERMISSION = "insufficient_permissions"
ERROR_TYPE_SESSION_NOT_FOUND = "session_not_found"
ERROR_TYPE_GAME_STATE = "game_state_error"
ERROR_TYPE_INCORRECT_JSON_FORMAT = "incorrect_json"

ONLY_HOST_CAN_START_MESSAGE = "Only the host can start the game"
INVALID_PLAYER_ID_MESSAGE = "The player id that was provided is not valid"
GAME_SESSION_CREATED_MESSAGE = "Successfully created a new game session."
GAME_SESSION_NOT_FOUND_MESSAGE = "This game session could not be found!"
PLAYER_JOINED_MESSAGE = "Player joined a game session"
PLAYER_ELIMINATED_MESSAGE = "You are eliminated and can't play anymore"
INCORRECT_TYPE_MESSAGE = "Incorrect message type"
NOT_ENOUGH_PLAYERS_MESSAGE = "The game can not be started with less than 3 players"
GAME_STARTING_FROM_WRONG_STATE_MESSAGE = "The game can not be started from the current state"
JSON_DECODE_ERROR_MESSAGE = "The json you sent is not in the correct format!"
CONNECTION_CLOSED_MESSAGE = "Closing the current connection"
