import pygame
import pdb
import os
from Tile import *

window_height = 400
window_width = 400
frame_delay = 1000//60
board_height = 20
board_height_buffer = 2 # buffer for blocks that start above the top of the board
board_width = 10
tile_size = window_height // board_height
images = {}

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


	pygame.display.update()

def update_board():
	global board
	time_to_spawn = True
	if time_to_spawn:
		board[4][2] = Tile(1)
		time_to_spawn = False
	# if keys[pygame.K_LEFT]:
	# 	x -= tile_size
	# if keys[pygame.K_RIGHT]:
	# 	x += tile_size
	# if keys[pygame.K_UP]:
	# 	y -= tile_size
	# if keys[pygame.K_DOWN]:
	# 	y += tile_size


pygame.init()

load_images()
init_board()

logo = pygame.image.load('iconsmall.bmp')
pygame.display.set_icon(logo)
pygame.display.set_caption('Tetrisn\'t')

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((window_width, window_width))

# define a variable to control the main loop
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
	draw_board()