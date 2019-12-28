import pygame

DIRECTION_DOWN  = 0
DIRECTION_LEFT  = 1
DIRECTION_RIGHT = 2

CANT_MOVE_PIECE = 0
CANT_MOVE_BOARD = 1
CAN_MOVE = 2


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

TETRIS_STATE_SPAWN = 0
TETRIS_STATE_PLAY  = 1
TETRIS_STATE_CLEAR = 2

PLAYER_STATE_SPAWN = 0
PLAYER_STATE_PLAY  = 1
PLAYER_STATE_CLEAR = 2

BOARD_WIDTH  = 14 # cannot be less than 4
BOARD_HEIGHT = 20 # should be about twice BOARD_WIDTH

window_height = 800
window_width = 1000
board_height_buffer = 2
frame_rate = 60

fall_delay_values = {
	0:48,
	1:43,
	2:38,
	3:33,
	4:28,
	5:23,
	6:18,
	7:13,
	8:8,
	9:6,
	10:5,
	13:4,
	16:3,
	19:2,
	29:1
}

keybindings = {
# player,      left,       down,       right,      ccw,        cw
	0 : (pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_q, pygame.K_e),
	1 : (pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_u, pygame.K_o)
}
KEYBINDING_LEFT = 0
KEYBINDING_DOWN = 1
KEYBINDING_RIGHT = 2
KEYBINDING_CCW = 3
KEYBINDING_CW = 4









