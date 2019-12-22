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
	def get_event(self, event):
		pass
	def update(self, screen, dt):
		self.draw(screen)
	def draw(self, screen):
		screen.fill((100,255,0))

class Game(States):
	def __init__(self):
	
		States.__init__(self)
		
		self.next = 'menu'
		
		self.frame_delay_ms = 1000//frame_rate
		self.fall_delay = 49
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

		self.score = 31415
		self.time_to_spawn = False
		self.time_to_fall = False
		self.time_to_move = False
		self.time_to_rotate = False
		self.time_next_move = 0
		self.time_next_fall = 0
		self.time_next_rotate = 0
		self.has_cw_rotate_been_released = True
		self.has_ccw_rotate_been_released = True
		
		self.sprites = {}

		self.board = []

		# load sprites
		if getattr(sys, 'frozen', False):
			wd = sys._MEIPASS
		else:
			wd = ''
		# Load sprites from image files and convert for performance
		sprites[TILE_TYPE_BLANK] = pygame.image.load(os.path.join(wd,'backgroundblock.bmp')).convert()
		sprites[TILE_TYPE_IOT] = pygame.image.load(os.path.join(wd,'IOTblock.bmp')).convert()
		sprites[TILE_TYPE_JS] = pygame.image.load(os.path.join(wd,'JSblock.bmp')).convert()
		sprites[TILE_TYPE_LZ] = pygame.image.load(os.path.join(wd,'LZblock.bmp')).convert()

		# Fill board with empty tiles
		self.board = [[Tile() for j in range(board_width)] for i in range(board_height+board_height_buffer)]
				
		
	def get_event(self, event):
		pass
	def update(self, screen, dt):
		global board
		global score
		global active_piece
		global active_piece_type
		global next_piece
		global next_piece_type
		global time_to_spawn
		global time_to_fall
		global time_to_move
		global time_to_rotate
		global time_next_fall
		global time_next_move
		global time_next_rotate
		global has_cw_rotate_been_released
		global has_ccw_rotate_been_released

		ticks = pygame.time.get_ticks()


		if time_to_spawn:
			# RNG piece choice decision
			if next_piece_type == None:
				active_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			else:
				active_piece_type = copy(next_piece)
			next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
			if next_piece_type == active_piece_type:
				next_piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])

			active_piece = Piece(active_piece_type)
			next_piece   = Piece(next_piece_type)
			time_next_fall = ticks + 20 * fall_delay
			time_to_spawn = False
		if active_piece == None:
			time_to_spawn = True
			return

		if ticks >= time_next_move:
			time_to_move = True
			time_next_move = ticks + move_delay
		if ticks >= time_next_fall:
			time_to_fall = True
			time_next_fall = ticks + fall_delay
		if ticks >= time_next_rotate:
			time_to_rotate = True
			time_next_rotate = ticks + rotate_delay

		if not can_move(direction = DIRECTION_DOWN):
			for location in active_piece.locations:
				board[location[1]][location[0]] = Tile(active_piece.tile_type)
			active_piece = None
			clear_lines()
			return

		if time_to_fall:
			active_piece.move(direction = DIRECTION_DOWN)
			time_to_fall = False

		if time_to_move:
			if keys[pygame.K_a]:
				if can_move(direction = DIRECTION_LEFT):
					active_piece.move(direction = DIRECTION_LEFT)
			if keys[pygame.K_d]:
				if can_move(direction = DIRECTION_RIGHT):
					active_piece.move(direction = DIRECTION_RIGHT)
			if keys[pygame.K_s]:
				if can_move(direction = DIRECTION_DOWN):
					active_piece.move(direction = DIRECTION_DOWN)
			time_to_move = False

		if time_to_rotate and has_ccw_rotate_been_released and has_cw_rotate_been_released:
			if keys[pygame.K_LEFT]:
				if can_rotate(ROTATION_CCW):
					active_piece.rotate(ROTATION_CCW)
			if keys[pygame.K_RIGHT]:
				if can_rotate(ROTATION_CW):
					active_piece.rotate(ROTATION_CW)
			time_to_rotate = False

		if keys[pygame.K_LEFT]: # to make each rotation key press only rotate once
			has_ccw_rotate_been_released = False
		else:
			has_ccw_rotate_been_released = True

		if keys[pygame.K_RIGHT]:
			has_cw_rotate_been_released = False
		else:
			has_cw_rotate_been_released = True

		score += 1



		self.draw(screen)
	def draw(self, screen):
		screen.fill((0,0,0))
		for row_index, tile_row in enumerate(board):
			for col_index, tile in enumerate(tile_row):
				scaled_image = pygame.transform.scale(sprites[tile.tile_type], (tile_size, tile_size))
				screen.blit(scaled_image, (col*tile_size, row*tile_size))
				
		for location in active_piece.locations:
			scaled_image = pygame.transform.scale(sprites[active_piece.tile_type], (tile_size, tile_size))
			screen.blit(scaled_image, (location[0]*tile_size, location[1]*tile_size))

		for row_index in range(0,2):
			for col_index in range(0,4):
				for location in next_piece.locations:
					if location == (col_index,row_index):
						scaled_image = pygame.transform.scale(sprites[next_piece.tile_type], (tile_size, tile_size))
						screen.blit(scaled_image, ((location[0]+board_width+1)*tile_size, (location[1]+1)*tile_size))
			
class Control:
	def __init__(self, **settings):
		self.__dict__.update(settings)
		self.done = False
		self.screen = pygame.time.Clock()
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
	def event_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			self.state.get_event(event)
	def main_game_loop(self):
		while not self.done:
			delta_time = self.clock.tick(self.fps)/1000.0
			self.event_loop()
			self.update(delta_time)
			pygame.display.update()
			
settings = {
    'window_size':(400,400),
    'frame_rate' :60
	'board_width':10
	'board_height':20
	'board_height_buffer':0
}

program = Control(**settings)
state_dict = {
	'menu': Menu(),
	'game': Game()
}
program.setup_states(state_dict, 'game')
app.main_game_loop()
pygame.quit()
sys.exit()








# Check if piece can move in the specified direction
# Returns: True, False
def can_move(direction):

	# Check for intersections with other pieces
	if direction == DIRECTION_DOWN:
		for location in active_piece.locations:
			if location[1] + 2 > len(board):
				return False
			tile = board[location[1] + 1][location[0]]
			if tile.tile_type != TILE_TYPE_BLANK:
				return False

	if direction == DIRECTION_LEFT:
		for location in active_piece.locations:
			if location[0] <= 0:
				return False
			tile = board[location[1]][location[0] - 1]
			if tile.tile_type != TILE_TYPE_BLANK:
				return False

	if direction == DIRECTION_RIGHT:
		for location in active_piece.locations:
			if location[0] + 1 >= len(board[0]):
				return False
			tile = board[location[1]][location[0] + 1]
			if tile.tile_type != TILE_TYPE_BLANK:
				return False

	return True


def can_rotate(rotation_direction):
	if active_piece.piece_type == PIECE_TYPE_O: # for the meme
		return True
	elif active_piece.piece_type == PIECE_TYPE_Z: # the special case
		if active_piece.rotation in [0,180]:
			pivot = copy(active_piece.locations[1])
			if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]-1>=-2 and pivot[1]-1<=board_height-1: # self.locations[0] = (pivot[0]+1,pivot[1]-1)
				if board[pivot[1]-1][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[1] = (pivot[0]+1,pivot[1])
				if board[pivot[1]][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[2] = pivot
				if board[pivot[1]][pivot[0]].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[3] = (pivot[0],pivot[1]+1)
				if board[pivot[1]+1][pivot[0]].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
		elif active_piece.rotation in [90,270]:
			pivot = copy(active_piece.locations[2])
			if pivot[0]-1>=0 and pivot[0]-1<=board_width-1 and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[0] = (pivot[0]-1,pivot[1])
				if board[pivot[1]][pivot[0]-1].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]>=-2   and pivot[1]<=board_height-1:   # self.locations[1] = pivot
				if board[pivot[1]][pivot[0]].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]>=0   and pivot[0]<=board_width-1   and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[2] = (pivot[0],pivot[1]+1)
				if board[pivot[1]+1][pivot[0]].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
			if pivot[0]+1>=0 and pivot[0]+1<=board_width-1 and pivot[1]+1>=-2 and pivot[1]+1<=board_height-1: # self.locations[3] = (pivot[0]+1,pivot[1]+1)
				if board[pivot[1]+1][pivot[0]+1].tile_type != TILE_TYPE_BLANK:
					return False
			else:
				return False
		return True # no check returned False
	elif active_piece.piece_type == PIECE_TYPE_I or active_piece.piece_type == PIECE_TYPE_S: # the two-rotation-position pieces that aren't special
		if active_piece.piece_type == PIECE_TYPE_I:
			pivot = active_piece.locations[2]
			if active_piece.rotation in [0,180]:
				turn = TURN_CW # turn to vertical
			else:
				turn = TURN_CCW # turn to horizontal
		elif active_piece.piece_type == PIECE_TYPE_S:
			pivot = copy(active_piece.locations[0])
			if active_piece.rotation in [0,180]:
				turn = TURN_CCW # turn to vertical
			else:
				turn = TURN_CW # turn to horizontal
		if turn == TURN_CW:
			# General check if can rotate CW:
			for location in active_piece.locations:
				new_x = (pivot[1]-location[1])+pivot[0]
				new_y = (location[0]-pivot[0])+pivot[1]
				if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
					if board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
		elif turn == TURN_CCW:
			# General check if can rotate CCW:
			for location in active_piece.locations:
				new_x = (location[1]-pivot[1])+pivot[0]
				new_y = (pivot[0]-location[0])+pivot[1]
				if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
					if board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
		return True # no check returned False
	elif active_piece.piece_type == PIECE_TYPE_T or active_piece.piece_type == PIECE_TYPE_L or active_piece.piece_type == PIECE_TYPE_J: # the four-rotation-position pieces
		pivot = copy(active_piece.locations[1])
		if rotation_direction == ROTATION_CW:
			# General check if can rotate CW:
			for location in active_piece.locations:
				new_x = (pivot[1]-location[1])+pivot[0]
				new_y = (location[0]-pivot[0])+pivot[1]
				if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
					if board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
		elif rotation_direction == ROTATION_CCW:
			# General check if can rotate CCW:
			for location in active_piece.locations:
				new_x = (location[1]-pivot[1])+pivot[0]
				new_y = (pivot[0]-location[0])+pivot[1]
				if new_x>=0 and new_x<=board_width-1 and new_y>=-2 and new_y<=board_height-1: # self.locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
					if board[new_y][new_x].tile_type != TILE_TYPE_BLANK:
						return False
				else:
					return False
		return True # no check returned False


# Check if lines can be cleared, clear them, shift stuff down, update score
def clear_lines():

	global board
	
	# Store all lines that can be cleared
	lines_to_clear = []

	# Add all clearable lines to list
	for row_index, row in enumerate(board):
		can_clear = True
		for tile in row:
			if tile.tile_type == TILE_TYPE_BLANK:
				can_clear = False
		if can_clear:
			lines_to_clear.append(row_index)

	# Get clear tiles on board
	# for line in lines_to_clear:
		# for tile in board[line]:
			# tile.tile_type = TILE_TYPE_BLANK

	# Move upper lines down
	for line in lines_to_clear:
		board.pop(line)
		board = deque(board)
		board.appendleft([Tile() for j in range(board_width)])
		board = list(board)
		# board = [Tile() for j in range(board_width)] + board
		# board.append([Tile() for j in range(board_width)])


pygame.init()

load_sprites()
init_board()

logo = pygame.image.load('iconsmall.bmp')
pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')

running = True

# main loop
while running:
	# Delay the game and keep running at certain framerate
	updateClock().tick_busy_loop(frame_delay_ms)
	debug_string = str(updateClock().get_fps())

	# event handling, gets all event from the event queue
	for event in pygame.event.get():
		# only do something if the event is of type QUIT
		if event.type == pygame.QUIT:
			# change the value to False, to exit the main loop
			running = False

	keys = pygame.key.get_pressed()

	update_board()
	if active_piece != None:
		draw_board()

	draw_text()
	pygame.display.update()
