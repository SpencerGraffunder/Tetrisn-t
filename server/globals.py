from common.game_state import GameState
from server.connection import Connection
player_count = 1

current_level = 0

# height should be about twice the width
board_height = 10
board_width = 20

tick_rate = 60

state = GameState()

connection = Connection()
