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


board_width = 10
board_height = 20
window_height = 400
window_width = 400
board_height_buffer = 0
frame_rate = 60


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
		self.rotate_delay = 49
		self.move_delay = 16
		self.tile_size = window_height // board_height
		self.active_piece = None
		# stores the type of piece active_piece is and passes it to the Piece() function
		self.active_piece_type = None

		# stores Piece object that holds data about next piece
		self.next_piece = None

		# stores the type of piece next_piece is and passes it to the Piece() function
		self.next_piece_type = None

		self.score = 0
		self.time_to_spawn = False
		self.time_to_fall = False
		self.time_to_move = False
		self.time_to_rotate = False
		self.time_next_move = 0
		self.time_next_fall = 0
		self.time_next_rotate = 0
		self.das_counter = 0
		self.das_threshold = 0
		self.is_move_right_pressed = False
		self.is_move_left_pressed = False
		
		self.sprites = {}

		self.board = []

		# load sprites
		if getattr(sys, 'frozen', False):
			wd = sys._MEIPASS
		else:
			wd = ''
		# Load sprites from image files and convert for performance
		self.sprites[TILE_TYPE_BLANK] = pygame.image.load(os.path.join(wd,'backgroundblock.bmp')).convert()
		self.sprites[TILE_TYPE_IOT] = pygame.image.load(os.path.join(wd,'IOTblock.bmp')).convert()
		self.sprites[TILE_TYPE_JS] = pygame.image.load(os.path.join(wd,'JSblock.bmp')).convert()
		self.sprites[TILE_TYPE_LZ] = pygame.image.load(os.path.join(wd,'LZblock.bmp')).convert()

		# Fill board with empty tiles
		self.board = [[Tile() for j in range(board_width)] for i in range(board_height+board_height_buffer)]


	def do_event(self, event):
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True
			
			if self.active_piece != None:
				if self.time_to_rotate:
					if event.key == pygame.K_LEFT:
						if self.can_rotate(ROTATION_CCW):
							self.active_piece.rotate(ROTATION_CCW)
							self.time_to_rotate = False
					if event.key == pygame.K_RIGHT:
						if self.can_rotate(ROTATION_CW):
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
					if self.can_move(direction = DIRECTION_DOWN):
						self.active_piece.move(direction = DIRECTION_DOWN)
				self.time_to_move = False
				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				self.is_move_left_pressed = False
			if event.key == pygame.K_d:
				self.is_move_right_pressed = False
		

	# Check if piece can move in the specified direction
	# Returns: True, False
	def can_move(self, direction):

		# Check for intersections with other pieces
		if direction == DIRECTION_DOWN:
			for location in self.active_piece.locations:
				if location[1] + 2 > len(self.board):
					return False
				tile = self.board[location[1] + 1][location[0]]
				if tile.tile_type != TILE_TYPE_BLANK:
					return False

		if direction == DIRECTION_LEFT:
			for location in self.active_piece.locations:
				if location[0] <= 0:
					return False
				tile = self.board[location[1]][location[0] - 1]
				if tile.tile_type != TILE_TYPE_BLANK:
					return False

		if direction == DIRECTION_RIGHT:
			for location in self.active_piece.locations:
				if location[0] + 1 >= len(self.board[0]):
					return False
				tile = self.board[location[1]][location[0] + 1]
				if tile.tile_type != TILE_TYPE_BLANK:
					return False

		return True

	def can_rotate(self, rotation_direction):
		if self.active_piece.piece_type == PIECE_TYPE_O: # for the meme
			return True
		elif self.active_piece.piece_type == PIECE_TYPE_Z: # the special case
			if self.active_piece.rotation in [0,180]:
				pivot = copy(self.active_piece.locations[1])
				if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]-1>=-2 and pivot[1]-1<=board_height-1: # self.locations[0] = (pivot[0]+1,pivot[1]-1)
					if self.board[pivot[1]-1][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[1] = (pivot[0]+1,pivot[1])
					if self.board[pivot[1]][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[2] = pivot
					if self.board[pivot[1]][pivot[0]].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[3] = (pivot[0],pivot[1]+1)
					if self.board[pivot[1]+1][pivot[0]].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
			elif self.active_piece.rotation in [90,270]:
				pivot = copy(self.active_piece.locations[2])
				if pivot[0]-1>=0 and pivot[0]-1<=board_width-1 and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[0] = (pivot[0]-1,pivot[1])
					if self.board[pivot[1]][pivot[0]-1].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[1] = pivot
					if self.board[pivot[1]][pivot[0]].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[2] = (pivot[0],pivot[1]+1)
					if self.board[pivot[1]+1][pivot[0]].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
				if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[3] = (pivot[0]+1,pivot[1]+1)
					if self.board[pivot[1]+1][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
			return True # no check returned False
		elif self.active_piece.piece_type == PIECE_TYPE_I or self.active_piece.piece_type == PIECE_TYPE_S: # the two-rotation-position pieces that aren't special
			if self.active_piece.piece_type == PIECE_TYPE_I:
				pivot = self.active_piece.locations[2]
				if self.active_piece.rotation in [0,180]:
					turn = TURN_CW # turn to vertical
				else:
					turn = TURN_CCW # turn to horizontal
			elif self.active_piece.piece_type == PIECE_TYPE_S:
				pivot = copy(self.active_piece.locations[0])
				if self.active_piece.rotation in [0,180]:
					turn = TURN_CCW # turn to vertical
				else:
					turn = TURN_CW # turn to horizontal
			if turn == TURN_CW:
				# General check if can rotate CW:
				for location in self.active_piece.locations:
					new_x = (pivot[1]-location[1])+pivot[0]
					new_y = (location[0]-pivot[0])+pivot[1]
					if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
						if self.board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
							return False
					else:
						return False
			elif turn == TURN_CCW:
				# General check if can rotate CCW:
				for location in self.active_piece.locations:
					new_x = (location[1]-pivot[1])+pivot[0]
					new_y = (pivot[0]-location[0])+pivot[1]
					if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
						if self.board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
							return False
					else:
						return False
			return True # no check returned False
		elif self.active_piece.piece_type == PIECE_TYPE_T or self.active_piece.piece_type == PIECE_TYPE_L or self.active_piece.piece_type == PIECE_TYPE_J: # the four-rotation-position pieces
			pivot = copy(self.active_piece.locations[1])
			if rotation_direction == ROTATION_CW:
				# General check if can rotate CW:
				for location in self.active_piece.locations:
					new_x = (pivot[1]-location[1])+pivot[0]
					new_y = (location[0]-pivot[0])+pivot[1]
					if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
						if self.board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
							return False
					else:
						return False
			elif rotation_direction == ROTATION_CCW:
				# General check if can rotate CCW:
				for location in self.active_piece.locations:
					new_x = (location[1]-pivot[1])+pivot[0]
					new_y = (pivot[0]-location[0])+pivot[1]
					if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
						if self.board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
							return False
					else:
						return False
			return True # no check returned False

	# Check if lines can be cleared, clear them, shift stuff down, update score
	def clear_lines(self, level = 0):

		# Store all lines that can be cleared
		lines_to_clear = []

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
			self.board.appendleft([Tile() for j in range(board_width)])
			self.board = list(self.board)

		# Score the points
		num_lines = len(lines_to_clear)
		if num_lines == 0:
			pass
		elif num_lines == 1:
			self.score += 40 * (level + 1)
		elif num_lines == 2:
			self.score += 100 * (level + 1)
		elif num_lines == 3:
			self.score += 300 * (level + 1)
		elif num_lines == 4: # BOOM Tetrisn't
			self.score += 1200 * (level + 1)


	def update(self, screen, dt):
	
		if self.is_move_left_pressed or self.is_move_right_pressed:
			self.das_counter += 1
		
			if self.das_counter > self.das_threshold:
				if self.is_move_left_pressed:
					if self.can_move(DIRECTION_LEFT):
						self.active_piece.move(DIRECTION_LEFT)
				if self.is_move_right_pressed:
					if self.can_move(DIRECTION_RIGHT):
						self.active_piece.move(DIRECTION_RIGHT)
				self.das_counter = 0
				if self.das_threshold == 0:
					self.das_threshold = 16
				else:
					self.das_threshold = 6

		ticks = pygame.time.get_ticks()

		if self.time_to_spawn:
			# RNG piece choice decision
			if self.next_piece_type == None:
				self.active_piece_type = copy(random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S]))
			else:
				self.active_piece_type = copy(self.next_piece.piece_type)
			self.next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			if self.next_piece_type == self.active_piece_type:
				self.next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			# pdb.set_trace()
			self.active_piece = Piece(self.active_piece_type)
			self.next_piece   = Piece(self.next_piece_type)
			time_next_fall = ticks + 20 * self.fall_delay
			self.time_to_spawn = False
			
		if self.active_piece == None:
			self.time_to_spawn = True
			return

		if ticks >= self.time_next_move:
			self.time_to_move = True
			self.time_next_move = ticks + self.move_delay
		if ticks >= self.time_next_fall:
			self.time_to_fall = True
			self.time_next_fall = ticks + self.fall_delay
		if ticks >= self.time_next_rotate:
			self.time_to_rotate = True
			self.time_next_rotate = ticks + self.rotate_delay

		if not self.can_move(direction = DIRECTION_DOWN):
			for location in self.active_piece.locations:
				self.board[location[1]][location[0]] = Tile(self.active_piece.tile_type)
			self.active_piece = None
			self.clear_lines()
			return

		if self.time_to_fall:
			self.active_piece.move(direction = DIRECTION_DOWN)
			self.time_to_fall = False

		self.score += 1

		self.draw(screen)

	def draw(self, screen):
		screen.fill((0,0,0))
		for row_index, tile_row in enumerate(self.board):
			for col_index, tile in enumerate(tile_row):
				scaled_image = pygame.transform.scale(self.sprites[tile.tile_type], (self.tile_size, self.tile_size))
				screen.blit(scaled_image, (col_index * self.tile_size, row_index * self.tile_size))

		for location in self.active_piece.locations:
			scaled_image = pygame.transform.scale(self.sprites[self.active_piece.tile_type], (self.tile_size, self.tile_size))
			screen.blit(scaled_image, (location[0]*self.tile_size, location[1]*self.tile_size))

		for row_index in range(0,2):
			for col_index in range(0,4):
				for location in self.next_piece.locations:
					if location == (col_index, row_index):
						#pdb.set_trace()
						scaled_image = pygame.transform.scale(self.sprites[self.next_piece.tile_type], (self.tile_size, self.tile_size))
						screen.blit(scaled_image, ((location[0]+board_width+1)*self.tile_size, (location[1]+1)*self.tile_size))

class Control:
	def __init__(self):
		self.done = False
		self.screen = pygame.display.set_mode((window_height, window_width))
		self.clock = pygame.time.Clock()
		self.frame_delay_ms = 1000 // frame_rate
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