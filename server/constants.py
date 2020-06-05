import pygame
from collections import defaultdict


# Buffer for allowing pieces to be above the board when they spawn
BOARD_HEIGHT_BUFFER = 2

FALL_DELAY_VALUES = {
  # level: frames till fall
    0:  48,
    1:  43,
    2:  38,
    3:  33,
    4:  28,
    5:  23,
    6:  18,
    7:  13,
    8:  8,
    9:  6,
    10: 5,
    13: 4,
    16: 3,
    19: 2,
    29: 1
}

DAS_VALUES = defaultdict(lambda: (3, 8))
DAS_VALUES[1] = (6, 16)
