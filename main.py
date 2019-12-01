import pygame
import pdb
import os
from Tile import *
from Piece import *
import random
from tetrisnt_enums import *

window_height = 400
window_width = 400
frame_rate = 10
frame_delay = 1000//frame_rate
board_height = 20
board_height_buffer = 2 # buffer for blocks that start above the top of the board
board_width = 10
tile_size = window_height // board_height
images = {}
active_piece = None
score = 31415
debug_string = 'hello there'
time_to_spawn = False

# 2d array where all the tiles are stored, initialized with board_width * (board_height + board_height_buffer) blank tiles
# access with board[col][row]
board = []

def init_board():
	global board
	board = [[Tile() for j in range(board_width)] for i in range(board_height+board_height_buffer)]

def load_images():
	images[0] = pygame.image.load('backgroundblock.bmp')
	images[1] = pygame.image.load('ISTblock.bmp')

def draw_board():
	screen.fill((0,0,0))
	for row, tile_row in enumerate(board[2:]):
		for col, tile in enumerate(tile_row):				

			scaled_image = pygame.transform.scale(images[tile.tile_type], (tile_size, tile_size))
			screen.blit(scaled_image, (col*tile_size, row*tile_size))

	for location in active_piece.locations:
		scaled_image = pygame.transform.scale(images[1], (tile_size, tile_size))
		screen.blit(scaled_image, (location[0]*tile_size, location[1]*tile_size))


	

def draw_text():
	x = board_width * tile_size
	y = 0

	font = pygame.font.Font('freesansbold.ttf', 24) 

	score_text = font.render(str(score), True, (0,255,0))
	  
	screen.blit(score_text, (x,y))

	debug_text = font.render(str(debug_string), True, (255,0,0))

	screen.blit(debug_text, (x, score_text.get_height()))

def update_board():
	global board
	global score
	global active_piece
	global time_to_spawn
	
	if time_to_spawn:
		new_piece_type = random.randint(1,7+1)
		active_piece = Piece(PIECE_TYPE_I)
		time_to_spawn = False
	elif active_piece == None:
		time_to_spawn = True
		return

	# for location in active_piece.locations:
	# 	board[location[1]][location[0]] = Tile(tile_type = active_piece.piece_type, is_active = True)

	allow_movement = True
	if allow_movement:
		if keys[pygame.K_LEFT]:
			if can_move(direction = DIRECTION_LEFT):
				active_piece.move(direction = DIRECTION_LEFT)
		if keys[pygame.K_RIGHT]:
			if can_move(direction = DIRECTION_RIGHT):
				active_piece.move(direction = DIRECTION_RIGHT)
		if keys[pygame.K_DOWN]:
			if can_move(direction = DIRECTION_DOWN):
				active_piece.move(direction = DIRECTION_DOWN)



	global debug_string
	debug_string = ''
	for location in active_piece.locations:
		debug_string += str(location) + ' '
	score += 1

def can_move(direction = DIRECTION_DOWN):
	return True # remove when fixed
	# todo: insert logic to return True if none of the locations in piece would intersect a piece on the board after it were moved
	if direction == DIRECTION_DOWN: # down
		pass # do nothing
	if direction == DIRECTION_LEFT: # left
		pass # do nothing
	if direction == DIRECTION_RIGHT: # right
		pass # do nothing

	return False

def clear_lines():
	# todo: insert logic to check if line can be cleared and clear/move tiles
	pass # do nothing



pygame.init()

load_images()
init_board()

logo = pygame.image.load('iconsmall.bmp')
pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')

# thing that we draw to
screen = pygame.display.set_mode((window_width, window_width))


running = True

# main loop
while running:
	pygame.time.delay(frame_delay)

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