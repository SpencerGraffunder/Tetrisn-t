from common.player_input import ControlType
import pygame

# Number of players
local_player_count = 1

tick_rate = 60

# Window dimensions in pixels
window_height = 900
window_width = (34*window_height)//20

# Size of the board tiles on the screen in pixels
tile_size = None

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
        pygame.K_ESCAPE: ControlType.PAUSE},
    2: {pygame.K_j: ControlType.LEFT,
        pygame.K_l: ControlType.RIGHT,
        pygame.K_k: ControlType.DOWN,
        pygame.K_u: ControlType.CCW,
        pygame.K_o: ControlType.CW,
        pygame.K_ESCAPE: ControlType.PAUSE},
    3: {pygame.K_j: ControlType.LEFT,
        pygame.K_l: ControlType.RIGHT,
        pygame.K_k: ControlType.DOWN,
        pygame.K_u: ControlType.CCW,
        pygame.K_o: ControlType.CW,
        pygame.K_ESCAPE: ControlType.PAUSE}
}

#
tile_surfaces = [0]
