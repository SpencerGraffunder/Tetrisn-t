import pygame
from collections import defaultdict
from enum import Enum


class TileType(Enum):
    IOT   = 0
    JS    = 1
    LZ    = 2
    GRAY  = 3
    BLANK = 4
    X     = 5


class Direction(Enum):
    DOWN  = 0
    LEFT  = 1
    RIGHT = 2


class PieceType(Enum):
    I = 0
    O = 1
    T = 2
    L = 3
    J = 4
    S = 5
    Z = 6


class TetrisState(Enum):
    SPAWN_DELAY = 0
    SPAWN = 1
    PLAY = 2
    CHECK_CLEAR = 3
    CLEAR = 4
    DIE = 5
    GAME_OVER = 6


# Buffer for allowing pieces to be above the board when they spawn
BOARD_HEIGHT_BUFFER = 2

CANT_MOVE_PIECE = 0
CANT_MOVE_BOARD = 1
CAN_MOVE        = 2

ROTATION_CW  = 0
ROTATION_CCW = 1
TURN_CW      = 0
TURN_CCW     = 1

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
