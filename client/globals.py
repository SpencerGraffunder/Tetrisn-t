from common.player_input import ControlType
import pygame

# Number of players
local_player_count = 1

current_level = 0

# Should be about twice board_width
board_height = 20
board_width = 10

tick_rate = 60

# Window dimensions in pixels
window_height = 800
window_width = 1000

# Size of the board tiles on the screen in pixels
tile_size = min(window_width, window_height) // max(board_width, board_height)

keybindings = {
    0: {pygame.K_a: ControlType.LEFT,
        pygame.K_d: ControlType.RIGHT,
        pygame.K_s: ControlType.DOWN,
        pygame.K_q: ControlType.CCW,
        pygame.K_e: ControlType.CW,
        pygame.K_ESCAPE: ControlType.PAUSE},
    1: {pygame.K_j: ControlType.LEFT,
        pygame.K_l: ControlType.RIGHT,
        pygame.K_k: ControlType.DOWN,
        pygame.K_u: ControlType.CCW,
        pygame.K_o: ControlType.CW,
        pygame.K_ESCAPE: ControlType.PAUSE}
}