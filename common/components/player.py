from server.constants import *


class Player:
    def __init__(self, player_number):
    
        self.player_number = player_number

        # piece given
        self.active_piece    = None
        self.next_piece      = None
        self.next_piece_type = None

        # clear/spawn
        self.clear_animation_counter = 0
        self.spawn_delay_counter     = 0
        self.spawn_delay_threshold   = 10

        # piece movement
        self.fall_counter  = 0
        self.das_counter   = 0
        self.das_threshold = 0
        self.down_counter  = 0

        # controls
        self.is_move_right_pressed = False
        self.is_move_left_pressed  = False
        self.is_move_down_pressed  = False

        # state
        self.player_state   = TETRIS_STATE_SPAWN
        self.lines_to_clear = []

        # spawn column; set in server/states/game.py
        self.spawn_column = None
