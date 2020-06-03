import pygame
from collections import defaultdict

# Buffer for allowing pieces to be above the board when they spawn
BOARD_HEIGHT_BUFFER = 2

DIRECTION_DOWN  = 0
DIRECTION_LEFT  = 1
DIRECTION_RIGHT = 2

CANT_MOVE_PIECE = 0
CANT_MOVE_BOARD = 1
CAN_MOVE        = 2

ROTATION_CW  = 0
ROTATION_CCW = 1
TURN_CW      = 0
TURN_CCW     = 1

PIECE_TYPE_I = 0
PIECE_TYPE_O = 1
PIECE_TYPE_T = 2
PIECE_TYPE_L = 3
PIECE_TYPE_J = 4
PIECE_TYPE_S = 5
PIECE_TYPE_Z = 6

TILE_TYPE_BLANK        = 0
TILE_TYPE_IOT          = 1
TILE_TYPE_JS           = 2
TILE_TYPE_LZ           = 3
TILE_TYPE_GRAY         = 4
TILE_TYPE_GRAY_HLLEFT  = 5
TILE_TYPE_GRAY_HLRIGHT = 6
TILE_TYPE_GRAY_HLUP    = 7
TILE_TYPE_GRAY_HLDOWN  = 8

TETRIS_STATE_SPAWN_DELAY = 0
TETRIS_STATE_SPAWN       = 1
TETRIS_STATE_PLAY        = 2
TETRIS_STATE_CHECK_CLEAR = 3
TETRIS_STATE_CLEAR       = 4
TETRIS_STATE_DIE         = 5
TETRIS_STATE_GAME_OVER   = 6

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
DAS_VALUES[0] = (6, 16)
