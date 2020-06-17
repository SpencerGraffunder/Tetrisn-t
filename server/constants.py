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

SCORING_VALUES = defaultdict(lambda: SCORING_VALUES[max(SCORING_VALUES.keys())])
SCORING_VALUES[0] = 0
SCORING_VALUES[1] = 40
SCORING_VALUES[2] = 100
SCORING_VALUES[3] = 300
SCORING_VALUES[4] = 1200

# the DAS_VALUES constants are for das_threshold in server/states/game.py and it's 0-indexed so that we can use
# das_threshold = 0 to have the piece move immediately after a direction press
DAS_VALUES = defaultdict(lambda: (3 - 1, 8 - 1))
DAS_VALUES[1] = (6 - 1, 16 - 1)

SERVER_ADDR = '192.168.1.8'
SERVER_PORT = '42069'
