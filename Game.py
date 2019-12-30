import pygame
from States import *
import sys
import os
from Tile import * # Import like this to avoid having to do Tile. before everything
from Piece import *
from Player import *
import random
from collections import deque
from tetrisnt_enums import *
from Text import *

class Game(States):
	def __init__(self):

		States.__init__(self)

		self.next = 'menu'

		self.players = [Player(0), Player(1)]

		self.score = 0
		self.current_level = 0
		self.fall_threshold = FALL_DELAY_VALUES[self.current_level]
		self.fall_counter = 0
		self.time_to_move = False
		self.time_next_move = 0
		self.time_next_fall = 0
		self.time_next_rotate = 0
		self.das_counter = 0
		self.das_threshold = 0
		self.down_counter = 0
		self.is_move_right_pressed = False
		self.is_move_left_pressed = False
		self.is_move_down_pressed = False
		self.spawn_delay_counter = 0
		self.spawn_delay_threshold = 10
		self.clear_animation_counter = 0
		self.last_lock_position = 0
		self.lines_cleared = 10 * self.current_level
		self.die_counter = 0

		self.sprites = {}

		self.board = []

		# load sprites
		if getattr(sys, 'frozen', False):
			wd = sys._MEIPASS
		else:
			wd = ''
		# Load sprites from image files and convert for performance
		self.sprites[TILE_TYPE_BLANK]        = pygame.image.load(os.path.join(wd,'backgroundblock.bmp')).convert()
		self.sprites[TILE_TYPE_IOT]          = pygame.image.load(os.path.join(wd,'IOTblock.bmp')).convert()
		self.sprites[TILE_TYPE_JS]           = pygame.image.load(os.path.join(wd,'JSblock.bmp')).convert()
		self.sprites[TILE_TYPE_LZ]           = pygame.image.load(os.path.join(wd,'LZblock.bmp')).convert()
		self.sprites[TILE_TYPE_GRAY]         = pygame.image.load(os.path.join(wd,'grayHL/lightgray.bmp')).convert()
		self.sprites[TILE_TYPE_GRAY_HLLEFT]  = pygame.image.load(os.path.join(wd,'grayHL/grayHLleft.bmp')).convert()
		self.sprites[TILE_TYPE_GRAY_HLRIGHT] = pygame.image.load(os.path.join(wd,'grayHL/grayHLright.bmp')).convert()
		self.sprites[TILE_TYPE_GRAY_HLUP]    = pygame.image.load(os.path.join(wd,'grayHL/grayHLup.bmp')).convert()
		self.sprites[TILE_TYPE_GRAY_HLDOWN]  = pygame.image.load(os.path.join(wd,'grayHL/grayHLdown.bmp')).convert()

		# Fill board with empty tiles
		self.board = [[Tile() for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT+BOARD_HEIGHT_BUFFER)]


	def do_event(self, event, player_number):

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True

			if self.players[player_number].active_piece != None:
				if event.key == KEYBINDINGS[player_number][KEYBINDING_CCW]:
					if self.players[player_number].active_piece.can_rotate(self.board, self.players, ROTATION_CCW):
						self.players[player_number].active_piece.rotate(ROTATION_CCW)
						self.time_to_rotate = False
				if event.key == KEYBINDINGS[player_number][KEYBINDING_CW]:
					if self.players[player_number].active_piece.can_rotate(self.board, self.players, ROTATION_CW):
						self.players[player_number].active_piece.rotate(ROTATION_CW)
						self.time_to_rotate = False

				if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
					self.players[player_number].is_move_left_pressed = True
					self.players[player_number].das_threshold = 0
					self.players[player_number].das_counter = 0
				if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
					self.players[player_number].is_move_right_pressed = True
					self.players[player_number].das_threshold = 0
					self.das_counter = 0
				if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
					self.players[player_number].is_move_down_pressed = True
					self.players[player_number].down_counter = 0

		if event.type == pygame.KEYUP:
			if event.key == KEYBINDINGS[player_number][KEYBINDING_LEFT]:
				self.players[player_number].is_move_left_pressed = False
			if event.key == KEYBINDINGS[player_number][KEYBINDING_RIGHT]:
				self.players[player_number].is_move_right_pressed = False
			if event.key == KEYBINDINGS[player_number][KEYBINDING_DOWN]:
				self.players[player_number].is_move_down_pressed = False


	def lock_piece(self, player_number):
		piece_locked_into_another_piece = False
		max_row_index = 0
		for location in self.players[player_number].active_piece.locations:
			self.board[location[1]][location[0]] = Tile(self.players[player_number].active_piece.tile_type)
			if location[1] > max_row_index:
				max_row_index = location[1]
			if self.board[location[1]][location[0]].tile_type != TILE_TYPE_BLANK:
				piece_locked_into_another_piece = True

		if self.players[player_number].active_piece.piece_type == PIECE_TYPE_I:
			self.players[player_number].spawn_delay_threshold = ((max_row_index+2)//4)*2+10
		else:
			self.players[player_number].spawn_delay_threshold = ((max_row_index+1+2)//4)*2+10

		self.players[player_number].active_piece = None
		if piece_locked_into_another_piece == False:
			self.players[player_number].player_state = TETRIS_STATE_CHECK_CLEAR
		else:
			for player in self.players:
				player.player_state = TETRIS_STATE_DIE


	def update(self, screen, dt, player_number):

		# player_number = self.player_number

		keys = pygame.key.get_pressed()
		if not self.players[player_number].is_move_left_pressed:
			if keys[KEYBINDINGS[player_number][KEYBINDING_LEFT]]:
				self.players[player_number].is_move_left_pressed = True
				das_counter = 0

		if not self.players[player_number].is_move_right_pressed:
			if keys[KEYBINDINGS[player_number][KEYBINDING_RIGHT]]:
				self.players[player_number].is_move_right_pressed = True
				das_counter = 0

		if self.players[player_number].player_state == TETRIS_STATE_SPAWN:

			self.players[player_number].spawn_delay_counter += 1

			if self.players[player_number].spawn_delay_counter > self.players[player_number].spawn_delay_threshold:

				# Spawn piece
				# RNG piece choice decision
				if self.players[player_number].next_piece_type == None:
					active_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				else:
					active_piece_type = self.players[player_number].next_piece.piece_type
				self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				if self.players[player_number].next_piece_type == active_piece_type:
					self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				self.players[player_number].active_piece = Piece(active_piece_type, player_number)
				self.players[player_number].next_piece   = Piece(self.players[player_number].next_piece_type, player_number)
				self.players[player_number].player_state = TETRIS_STATE_PLAY
				self.players[player_number].fall_counter = 0
				self.players[player_number].spawn_delay_counter = 0

		if self.players[player_number].player_state == TETRIS_STATE_PLAY:
			# Move piece logic
			if self.players[player_number].is_move_left_pressed or self.players[player_number].is_move_right_pressed:
				self.players[player_number].das_counter += 1

				if self.players[player_number].das_counter > self.players[player_number].das_threshold:
					if self.players[player_number].is_move_left_pressed:
						if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_LEFT) == CAN_MOVE:
							self.players[player_number].active_piece.move(DIRECTION_LEFT)
							self.players[player_number].das_counter = 0
							if self.players[player_number].das_threshold == 0:
								self.players[player_number].das_threshold = 8
							else:
								self.players[player_number].das_threshold = 3
					if self.players[player_number].is_move_right_pressed:
						if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_RIGHT) == CAN_MOVE:
							self.players[player_number].active_piece.move(DIRECTION_RIGHT)
							self.players[player_number].das_counter = 0
							if self.players[player_number].das_threshold == 0:
								self.players[player_number].das_threshold = 8
							else:
								self.players[player_number].das_threshold = 3

			if self.players[player_number].is_move_down_pressed:
				self.players[player_number].down_counter += 1

				if self.players[player_number].down_counter > 2:
					if self.players[player_number].is_move_down_pressed:
						if self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CAN_MOVE:
							self.players[player_number].active_piece.move(DIRECTION_DOWN)
							self.players[player_number].fall_counter = 0
						elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
							self.lock_piece(player_number)
						elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
							pass

						self.players[player_number].down_counter = 0

			self.players[player_number].fall_counter += 1

			if self.players[player_number].fall_counter >= self.fall_threshold and self.players[player_number].active_piece != None:
				if   self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_BOARD:
					self.lock_piece(player_number)
				elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CAN_MOVE:
					self.players[player_number].active_piece.move(DIRECTION_DOWN)
				elif self.players[player_number].active_piece.can_move(self.board, self.players, DIRECTION_DOWN) == CANT_MOVE_PIECE:
					pass
				self.players[player_number].fall_counter = 0


		elif self.players[player_number].player_state == TETRIS_STATE_CHECK_CLEAR:
			# Store all lines that can be cleared
			self.players[player_number].lines_to_clear = []

			self.players[player_number].is_move_down_pressed = False

			# Add all clearable lines to list
			for row_index, row in enumerate(self.board):
				can_clear = True
				for tile in row:
					if tile.tile_type == TILE_TYPE_BLANK:
						can_clear = False
				if can_clear:
					self.players[player_number].lines_to_clear.append(row_index)

			if len(self.players[player_number].lines_to_clear) > 0:
				self.players[player_number].player_state = TETRIS_STATE_CLEAR
				self.clear_animation_counter = 0
			elif len(self.players[player_number].lines_to_clear) == 0:
				self.players[player_number].player_state = TETRIS_STATE_SPAWN_DELAY


		if self.players[player_number].player_state == TETRIS_STATE_CLEAR:
			animation_length = self.spawn_delay_threshold + 20
			self.clear_animation_counter += 1

			if self.clear_animation_counter >= animation_length:
				# Move upper lines down
				for line in self.players[player_number].lines_to_clear:
					self.board.pop(line)
					self.board = deque(self.board)
					self.board.appendleft([Tile() for j in range(BOARD_WIDTH)])
					self.board = list(self.board)

				# Score the points
				num_lines = len(self.players[player_number].lines_to_clear)
				if num_lines != 0:
					if num_lines == 1:
						self.score += 40 * (self.current_level + 1)
					elif num_lines == 2:
						self.score += 100 * (self.current_level + 1)
					elif num_lines == 3:
						self.score += 300 * (self.current_level + 1)
					elif num_lines == 4: # BOOM Tetrisn't for Jeffn't
						self.score += 1200 * (self.current_level + 1)

					self.lines_cleared += len(self.players[player_number].lines_to_clear)
					if self.lines_cleared // 10 >= self.current_level + 1:
						self.current_level += 1

					if self.current_level in FALL_DELAY_VALUES.keys():
						self.fall_threshold = FALL_DELAY_VALUES[self.current_level]

				self.players[player_number].player_state = TETRIS_STATE_SPAWN

		elif self.players[player_number].player_state == TETRIS_STATE_SPAWN_DELAY:
			self.spawn_delay_counter += 1

			if self.spawn_delay_counter > self.spawn_delay_threshold:
				self.players[player_number].player_state = TETRIS_STATE_SPAWN

		if self.players[player_number].player_state == TETRIS_STATE_SPAWN:
			# Spawn piece
			# RNG piece choice decision
			if self.players[player_number].next_piece_type == None:
				active_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			else:
				active_piece_type = self.players[player_number].next_piece.piece_type
			self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			if self.players[player_number].next_piece_type == active_piece_type:
				self.players[player_number].next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			self.players[player_number].active_piece = Piece(active_piece_type, player_number)
			self.players[player_number].next_piece   = Piece(self.players[player_number].next_piece_type, player_number)
			self.players[player_number].player_state = TETRIS_STATE_PLAY
			self.players[player_number].fall_counter = 0
			self.players[player_number].spawn_delay_counter = 0

		if self.players[player_number].player_state == TETRIS_STATE_DIE:
			self.die_counter += 1
			if self.die_counter >= 120: # wait 2 seconds
				for player in self.players:
					player.player_state = TETRIS_STATE_GAME_OVER

		if self.players[player_number].player_state == TETRIS_STATE_GAME_OVER:
			self.next = 'game over'
			self.done = True


		self.draw(screen)

	def draw(self, screen):

		screen.fill((150, 150, 150))

		centering_offset = (WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH)) // 2

		# fill right of board with gray for background
		# for col_index in range(0+BOARD_WIDTH-1, 10+BOARD_WIDTH):
		# 	for row_index in range(0, BOARD_HEIGHT):
		# 		if col_index not in range(0+BOARD_WIDTH-1+4, 0+BOARD_WIDTH-1+8) or row_index not in range(1, 3):
		# 			scaled_image = pygame.transform.scale(self.sprites[TILE_TYPE_GRAY], (TILE_SIZE, TILE_SIZE))
		# 			screen.blit(scaled_image, (col_index * TILE_SIZE, row_index * TILE_SIZE))

		for row_index, tile_row in enumerate(self.board[2:]):
			for col_index, tile in enumerate(tile_row):
				scaled_image = pygame.transform.scale(self.sprites[tile.tile_type], (TILE_SIZE, TILE_SIZE))
				screen.blit(scaled_image, (col_index * TILE_SIZE + centering_offset, row_index * TILE_SIZE))

		for player in self.players:

			# to determine spawn positions
			if BOARD_WIDTH % 2 == 0: # even board width
				center = BOARD_WIDTH // 2
			elif BOARD_WIDTH % 2 == 1: # odd board width
				center = (BOARD_WIDTH+1) // 2


			if player.active_piece != None:
				for location in player.active_piece.locations:
					scaled_image = pygame.transform.scale(self.sprites[player.active_piece.tile_type], (TILE_SIZE, TILE_SIZE))
					screen.blit(scaled_image, (location[0] * TILE_SIZE + centering_offset, (location[1] - BOARD_HEIGHT_BUFFER) * TILE_SIZE))

		# Offset from center of screen to start drawing the next piece
		p0_offset = - ((BOARD_WIDTH // 2) * TILE_SIZE) - (5 * TILE_SIZE)
		p1_offset =    (BOARD_WIDTH // 2) * TILE_SIZE  + (1 * TILE_SIZE)
		center_screen = WINDOW_WIDTH // 2

		if self.players[0].next_piece != None:
			# draw next piece
			for row_index in range(2, 6):
				for col_index in range(2, 6):
					for location in self.players[0].next_piece.locations:
						if location == (col_index, row_index):
							scaled_image = pygame.transform.scale(self.sprites[self.players[0].next_piece.tile_type], (TILE_SIZE, TILE_SIZE))
							x = center_screen + p0_offset + ((location[0] - 2) * TILE_SIZE)
							y = (location[1] - 1) * TILE_SIZE
							screen.blit(scaled_image, (x, y))

		if self.players[1].next_piece != None:
			for row_index in range(2, 4):
				for col_index in range(8, 12):
					for location in self.players[1].next_piece.locations:
						if location == (col_index, row_index):
							scaled_image = pygame.transform.scale(self.sprites[self.players[1].next_piece.tile_type], (TILE_SIZE, TILE_SIZE))
							x = center_screen + p1_offset + ((location[0] - 8) * TILE_SIZE)
							y = (location[1] - 1) * TILE_SIZE
							screen.blit(scaled_image, (x, y))

		# draw purdy stuff
		# leftHL_locations = [()]

		# display score
		score_str1 = 'Score:'
		text.draw(screen, score_str1, 'SMALL', ((WINDOW_WIDTH) - (4 * TILE_SIZE), (BOARD_HEIGHT - 3) * TILE_SIZE), (0, 128, 0))

		score_str2 = '%d' % (self.score)
		text.draw(screen, score_str2, 'SMALL',  ((WINDOW_WIDTH) - (4 * TILE_SIZE), (BOARD_HEIGHT - 2) * TILE_SIZE), (0, 128, 0))

		# display level
		level_str = 'Level: %d' % (self.current_level)
		text.draw(screen, level_str, 'SMALL', ((WINDOW_WIDTH) - (4 * TILE_SIZE), (BOARD_HEIGHT - 4) * TILE_SIZE), (0, 128, 0))
