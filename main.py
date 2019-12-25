import pygame
import pdb
import os
from Tile import * # Import like this to avoid having to do Tile. before everything
from Piece import *
import random
from tetrisnt_enums import *
from copy import copy
from collections import deque
import sys


window_height = 800
window_width = 800
board_height_buffer = 2
frame_rate = 60

fall_delay_values = {
	0:48,
	1:43,
	2:38,
	3:33,
	4:28,
	5:23,
	6:18,
	7:13,
	8:8,
	9:6,
	10:5,
	13:4,
	16:3,
	19:2,
	29:1
}


class States(object):

	def __init__(self):
		self.done = False
		self.next = None
		self.quit = False
		self.previous = None

		
class Menu(States):

	def __init__(self):
		States.__init__(self)
		self.next = 'game'
		self.font = pygame.font.Font('freesansbold.ttf', 72)
		self.text = self.font.render('Tetrisn\'t', True, (0, 128, 0))
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (window_width//2, window_height//2)

	def do_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.done = True
			if event.key == pygame.K_ESCAPE:
				self.quit = True

	def update(self, screen, dt):
		self.draw(screen)

	def draw(self, screen):
		screen.fill((100,255,0))
		screen.blit(self.text, self.text_rect)
		

class Game(States):
	def __init__(self):

		States.__init__(self)

		self.next = 'menu'

		self.fall_delay = 150
		self.tile_size = window_height // BOARD_HEIGHT
		self.active_piece = None
		# stores the type of piece active_piece is and passes it to the Piece() function
		self.active_piece_type = None

		# stores Piece object that holds data about next piece
		self.next_piece = None

		# stores the type of piece next_piece is and passes it to the Piece() function
		self.next_piece_type = None

		self.score = 0
		self.current_level = 0
		self.time_to_fall = False
		self.fall_threshold = fall_delay_values[self.current_level]
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
		self.tetris_state = TETRIS_STATE_SPAWN
		self.last_lock_position = 0

		
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
		self.board = [[Tile() for j in range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT+board_height_buffer)]


	def do_event(self, event):
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True
			
			if self.active_piece != None:
				if event.key == pygame.K_LEFT:
					if self.active_piece.can_rotate(self.board, ROTATION_CCW):
						self.active_piece.rotate(ROTATION_CCW)
						self.time_to_rotate = False
				if event.key == pygame.K_RIGHT:
					if self.active_piece.can_rotate(self.board, ROTATION_CW):
						self.active_piece.rotate(ROTATION_CW)
						self.time_to_rotate = False
						
				if event.key == pygame.K_a:
					self.is_move_left_pressed = True
					self.das_threshold = 0
					self.das_counter = 0
				if event.key == pygame.K_d:
					self.is_move_right_pressed = True
					self.das_threshold = 0
					self.das_counter = 0
				if event.key == pygame.K_s:
					self.is_move_down_pressed = True
					self.down_counter = 0
				self.time_to_move = False
				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				self.is_move_left_pressed = False
			if event.key == pygame.K_d:
				self.is_move_right_pressed = False
			if event.key == pygame.K_s:
				self.is_move_down_pressed = False


	def lock_piece(self):

		max_row_index = 0
		for location in self.active_piece.locations:
			self.board[location[1]][location[0]] = Tile(self.active_piece.tile_type)
			if location[1] > max_row_index:
				max_row_index = location[1]

		if self.active_piece.piece_type == PIECE_TYPE_I:
			self.spawn_delay_threshold = ((max_row_index+2)//4)*2+10
		else:
			self.spawn_delay_threshold = ((max_row_index+1+2)//4)*2+10

		self.active_piece = None
		self.tetris_state = TETRIS_STATE_CLEAR


	def update(self, screen, dt):

		keys = pygame.key.get_pressed()
		if not self.is_move_left_pressed:
			if keys[pygame.K_a]:
				self.is_move_left_pressed = True
				das_counter = 0

		if not self.is_move_right_pressed:
			if keys[pygame.K_d]:
				self.is_move_right_pressed = True
				das_counter = 0

		if self.tetris_state == TETRIS_STATE_SPAWN:

			self.spawn_delay_counter += 1

			if self.spawn_delay_counter > self.spawn_delay_threshold:

				# Spawn piece
				# RNG piece choice decision
				if self.next_piece_type == None:
					self.active_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				else:
					self.active_piece_type = self.next_piece.piece_type
				self.next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				if self.next_piece_type == self.active_piece_type:
					self.next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
				self.active_piece = Piece(self.active_piece_type)
				self.next_piece   = Piece(self.next_piece_type)
				self.tetris_state = TETRIS_STATE_PLAY
				self.fall_counter = 0
				self.spawn_delay_counter = 0

		elif self.tetris_state == TETRIS_STATE_PLAY:
			# Move piece logic
			if self.is_move_left_pressed or self.is_move_right_pressed:
				self.das_counter += 1
			
				if self.das_counter > self.das_threshold:
					if self.is_move_left_pressed:
						if self.active_piece.can_move(self.board, DIRECTION_LEFT):
							self.active_piece.move(DIRECTION_LEFT)
							self.das_counter = 0
					if self.is_move_right_pressed:
						if self.active_piece.can_move(self.board, DIRECTION_RIGHT):
							self.active_piece.move(DIRECTION_RIGHT)
							self.das_counter = 0

					if self.das_threshold == 0:
						self.das_threshold = 16
					else:
						self.das_threshold = 6
						
			if self.is_move_down_pressed:
				self.down_counter += 1
				
				if self.down_counter > 2:
					if self.is_move_down_pressed:
						if self.active_piece.can_move(self.board, DIRECTION_DOWN):
							self.active_piece.move(DIRECTION_DOWN)
							self.fall_counter = 0
						else:
							self.lock_piece()
							
						self.down_counter = 0

			self.fall_counter += 1

			if self.fall_counter > self.fall_threshold and self.active_piece != None:
				if not self.active_piece.can_move(self.board, DIRECTION_DOWN):
					self.lock_piece()
				else:
					self.active_piece.move(DIRECTION_DOWN)

				self.fall_counter = 0


		elif self.tetris_state == TETRIS_STATE_CLEAR:
			# Store all lines that can be cleared
			lines_to_clear = []

			self.is_move_down_pressed = False

			# Add all clearable lines to list
			for row_index, row in enumerate(self.board):
				can_clear = True
				for tile in row:
					if tile.tile_type == TILE_TYPE_BLANK:
						can_clear = False
				if can_clear:
					lines_to_clear.append(row_index)
					
			# Move upper lines down
			for line in lines_to_clear:
				self.board.pop(line)
				self.board = deque(self.board)
				self.board.appendleft([Tile() for j in range(BOARD_WIDTH)])
				self.board = list(self.board)

			# Score the points
			num_lines = len(lines_to_clear)
			if num_lines != 0:
				if num_lines == 1:
					self.score += 40 * (self.current_level + 1)
				elif num_lines == 2:
					self.score += 100 * (self.current_level + 1)
				elif num_lines == 3:
					self.score += 300 * (self.current_level + 1)
				elif num_lines == 4: # BOOM Tetrisn't for Jeffn't
					self.score += 1200 * (self.current_level + 1)
					
				self.current_level += 1
				
				if self.current_level in fall_delay_values.keys():
					self.fall_threshold = fall_delay_values[self.current_level]
			self.tetris_state = TETRIS_STATE_SPAWN

		self.draw(screen)

	def draw(self, screen):

		center = 2

		# to determine spawn positions
		width = BOARD_WIDTH
		if width % 2 == 0: # even board width
			center = width // 2
		elif width % 2 == 1: # odd board width
			center = (width+1) // 2

		screen.fill((0, 0, 0))

		# fill right of board with gray for background
		for col_index in range(0+BOARD_WIDTH-1, 10+BOARD_WIDTH):
			for row_index in range(0, BOARD_HEIGHT):
				if col_index not in range(0+BOARD_WIDTH-1+4, 0+BOARD_WIDTH-1+8) or row_index not in range(1, 3):
					scaled_image = pygame.transform.scale(self.sprites[TILE_TYPE_GRAY], (self.tile_size, self.tile_size))
					screen.blit(scaled_image, (col_index * self.tile_size, row_index * self.tile_size))

		for row_index, tile_row in enumerate(self.board[2:]):
			for col_index, tile in enumerate(tile_row):
				scaled_image = pygame.transform.scale(self.sprites[tile.tile_type], (self.tile_size, self.tile_size))
				screen.blit(scaled_image, (col_index * self.tile_size, row_index * self.tile_size))

		if self.active_piece != None:
			for location in self.active_piece.locations:
				scaled_image = pygame.transform.scale(self.sprites[self.active_piece.tile_type], (self.tile_size, self.tile_size))
				screen.blit(scaled_image, (location[0] * self.tile_size, (location[1] - board_height_buffer) * self.tile_size))

		if self.next_piece != None:
			# draw next piece
			for row_index in range(2, 4):
				for col_index in range(center-2, center+1+1):
					for location in self.next_piece.locations:
						if location == (col_index, row_index):
							scaled_image = pygame.transform.scale(self.sprites[self.next_piece.tile_type], (self.tile_size, self.tile_size))
							screen.blit(scaled_image, ((location[0] + 5 + BOARD_WIDTH//2) * self.tile_size, (location[1] - 1) * self.tile_size))

		# draw purdy stuff
		# leftHL_locations = [()]

		# display score
		score_str = 'Score: %d' % (self.score)
		score_text_font        = pygame.font.Font('freesansbold.ttf', 20)
		score_text             = score_text_font.render(score_str, True, (0, 128, 0))
		score_text_rect        = score_text.get_rect()
		score_text_rect.center = ((BOARD_WIDTH + 4) * self.tile_size, 3.5 * self.tile_size)
		screen.blit(score_text, score_text_rect)

		# display level
		level_str = 'Level: %d' % (self.current_level)
		level_text_font        = pygame.font.Font('freesansbold.ttf', 20)
		level_text             = level_text_font.render(level_str, True, (0, 128, 0))
		level_text_rect        = level_text.get_rect()
		level_text_rect.center = ((BOARD_WIDTH + 4) * self.tile_size, 4 * self.tile_size)
		screen.blit(level_text, level_text_rect)


class Control:
	def __init__(self):
		self.done = False
		self.screen = pygame.display.set_mode((window_height, window_width))
		self.clock = pygame.time.Clock()
	def setup_states(self, state_dict, start_state):
		self.state_dict = state_dict
		self.state_name = start_state
		self.state = self.state_dict[self.state_name]
	def update(self, dt):
		if self.state.quit:
			self.done = True
		elif self.state.done:
			self.flip_state()
		self.state.update(self.screen, dt)
	def flip_state(self):
		self.state.done = False
		previous, self.state_name = self.state_name, self.state.next
		self.state = self.state_dict[self.state_name]
		self.state.previous = previous
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			self.state.do_event(event)
	def main_game_loop(self):
		while not self.done:
			delta_time = self.clock.tick(frame_rate)/1000.0
			self.event_loop()
			self.update(delta_time)
			pygame.display.update()

pygame.init()
program = Control()

state_dict = {
	'menu': Menu(),
	'game': Game()
}

logo = pygame.image.load('iconsmall.bmp')
pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')
program.setup_states(state_dict, 'game')
program.main_game_loop()
pygame.quit()
sys.exit()