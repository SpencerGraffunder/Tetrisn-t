from tetrisnt_enums import *
import pygame


class Player:

	def __init__(self, player_number):
		self.active_piece = None

		self.next_piece = None

		self.next_piece_type = None
		
		self.fall_counter = 0
		self.player_number = player_number

		self.das_counter = 0
		self.das_threshold = 0
		self.down_counter = 0
		self.is_move_right_pressed = False
		self.is_move_left_pressed = False
		self.is_move_down_pressed = False

		self.spawn_delay_counter = 0
		self.spawn_delay_threshold = 10

		self.player_state = PLAYER_STATE_SPAWN
		
		self.lines_to_clear = []
		self.have_lines_shifted = False

