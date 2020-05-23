from lib.Connection import Connection
import lib.Constants as Constants
#################
###  GLOBALS  ###
#################

PLAYER_COUNT = 1
GAME_JUST_STARTED = False

SINGLE_PLAYER_BOARD_WIDTH = 10
MULTI_PLAYER_BOARD_WIDTH = 14
BOARD_HEIGHT = 20 # should be about twice BOARD_WIDTH



BOARD_HEIGHT_BUFFER = 2
FRAME_RATE = 60

TILE_SIZE = min(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT) // max(SINGLE_PLAYER_BOARD_WIDTH,BOARD_HEIGHT)

connection = Connection()