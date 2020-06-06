from common.player_input import ControlType
import pygame
from collections import defaultdict
from client.constants import *

# Number of players
local_player_count = 1
player_count = 1

tick_rate = 60

# Window dimensions in pixels
window_height = 900
window_width = (((4*MAX_PLAYER_COUNT)+18)*window_height)//20

# Size of the board tiles on the screen in pixels
tile_size = None

keybindings = defaultdict(lambda: keybindings[0])
keybindings[0] = {pygame.K_a: ControlType.LEFT,
                  pygame.K_d: ControlType.RIGHT,
                  pygame.K_s: ControlType.DOWN,
                  pygame.K_q: ControlType.CCW,
                  pygame.K_e: ControlType.CW,
                  pygame.K_ESCAPE: ControlType.PAUSE}
keybindings[1] = {pygame.K_f: ControlType.LEFT,
                  pygame.K_h: ControlType.RIGHT,
                  pygame.K_g: ControlType.DOWN,
                  pygame.K_r: ControlType.CCW,
                  pygame.K_y: ControlType.CW,
                  pygame.K_ESCAPE: ControlType.PAUSE}
keybindings[2] = {pygame.K_j: ControlType.LEFT,
                  pygame.K_l: ControlType.RIGHT,
                  pygame.K_k: ControlType.DOWN,
                  pygame.K_u: ControlType.CCW,
                  pygame.K_o: ControlType.CW,
                  pygame.K_ESCAPE: ControlType.PAUSE}

# The graphics surfaces that will be drawn for each of the different tile types
tile_surfaces = {}
