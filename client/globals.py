import lib.Constants as Constants

# Import with:
# import Globals
# Not:
# from Globals import *

# Number of players
local_player_count = 1

CURRENT_LEVEL = 0

# Variable to tell Game to reset the board
GAME_JUST_STARTED = False

# Should be about twice BOARD_WIDTH
BOARD_HEIGHT = 20
BOARD_WIDTH = 10

BOARD_HEIGHT_BUFFER = 2
FRAME_RATE = 60

# Window dimensions in pixels
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000

# Size of the board tiles on the screen in pixels
tile_size = min(WINDOW_WIDTH,WINDOW_HEIGHT) // max(BOARD_WIDTH,BOARD_HEIGHT)

