from tetrisnt_enums import *


class Player:

	def __init__(self):
		self.active_piece = None

		self.next_piece = None

		self.next_piece_type = None

		self.time_to_fall = False
		self.fall_threshold = fall_delay_values[0]
		self.fall_counter = 0

		self.time_to_move = False
		self.das_counter = 0
		self.das_threshold = 0
		self.down_counter = 0
		self.is_move_right_pressed = False
		self.is_move_left_pressed = False
		self.is_move_down_pressed = False

		self.spawn_delay_counter = 0
		self.spawn_delay_threshold = 10