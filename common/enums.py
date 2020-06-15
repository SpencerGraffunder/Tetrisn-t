from enum import Enum


class TileType(Enum):
    IOT   = 0
    JS    = 1
    LZ    = 2
    GRAY  = 3
    BLANK = 4
    X     = 51


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


class Rotation(Enum):
    CW  = 0
    CCW = 1


class Turn(Enum):
    CW  = 0
    CCW = 1


class MoveAllowance(Enum):
    CANT_PIECE = 0
    CANT_BOARD = 1
    CAN        = 2
