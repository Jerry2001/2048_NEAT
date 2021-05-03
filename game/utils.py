from enum import Enum

# Enums to keep things persistence
class State(Enum):
    MENU = "menu"
    IDLE = "idle"
    SHIFTING = "shifting"
    WIN = "win"
    LOSS = "loss"


class Key(Enum):
    UP = "W"
    DOWN = "S"
    LEFT = "A"
    RIGHT = "D"
    RESTART = "R"
    BACK = "B"
    ENTER = "Enter"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


direction_mapping = {None: None, Key.UP: Direction.UP, Key.DOWN: Direction.DOWN, Key.LEFT: Direction.LEFT, Key.RIGHT: Direction.RIGHT}
key_mapping = {None: None, "w": Key.UP, "s": Key.DOWN, "a": Key.LEFT, "d": Key.RIGHT}


def key_to_direction(key):
    return direction_mapping[key]


def char_to_key(char):
    return key_mapping[char]


def char_to_direction(char):
    return direction_mapping[key_mapping[char]]


# Color set
BACKGROUND = (146,135,125)
ZERO = (205, 193, 180)
TWO = (238, 228, 218)
FOUR = (237, 224, 200)
EIGHT = (242, 177, 121)
ONE_SIX = (245, 124, 59)
THREE_TWO = (246, 124, 95)
SIX_FOUR = (246, 94, 59)
ONE_TWO_EIGHT = (237, 207, 114)
TWO_FIVE_SIX = (237, 204, 97)
FIVE_ONE_TWO = (237, 200, 80)
ONE_ZERO_TWO_FOUR = (237, 197, 63)
TWO_ZERO_FOUR_EIGHT = (237, 194, 46)

# Using None key for default color
colors = {None: BACKGROUND, 0: ZERO, 2: TWO, 4: FOUR, 8: EIGHT, 16: ONE_SIX, 32: THREE_TWO, 64: SIX_FOUR, 128: ONE_TWO_EIGHT,
          256: TWO_FIVE_SIX, 512: FIVE_ONE_TWO, 1024: ONE_ZERO_TWO_FOUR, 2048: TWO_ZERO_FOUR_EIGHT}


def get_colour(i):
    try:
        return colors[i]
    except KeyError:
        return colors[None]


# 2D array, rotates by 90 degrees
def rotate_clockwise(arr, iteration = 1):
    if iteration <= 0:
        return

    l = len(arr)
    for i in range(0, iteration):
        for s in range(0, int(l / 2)):
            for j in range(0, l - (2 * s) - 1):
                temp = arr[s][s + j]
                arr[s][s + j] = arr[l - s - j - 1][s]
                arr[l - s - j - 1][s] = arr[l - s - 1][l - s - j - 1]
                arr[l - s - 1][l - s - j - 1] = arr[s + j][l - s - 1]
                arr[s + j][l - s - 1] = temp

    return arr





