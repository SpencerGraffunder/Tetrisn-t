from lib.Constants import *
import lib.Globals as Globals
import pygame

class Player:

	def __init__(self, player_number, board_width):
	
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

		# split the board into PLAYER_COUNT equal sections (using floats), find the middle of the section we care about using the average, and favor right via the columns being index by 0
		self.spawn_column = int(((board_width / Globals.PLAYER_COUNT) * player_number + (board_width / Globals.PLAYER_COUNT) * (player_number + 1)) / 2)