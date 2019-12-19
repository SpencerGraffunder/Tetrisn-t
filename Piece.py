from tetrisnt_enums import *
import pdb
import random

previous_piece = None

class Piece:
	piece_type = 0
	tile_type = 0
	rotation = 0
	locations = [(0,0),(0,0),(0,0),(0,0)] # col,row

	def __init__(self):
		self.piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
		previous_piece = self.piece_type
		self.rotation = 0
		if self.piece_type == PIECE_TYPE_I:
			self.locations[0] = (3,0)
			self.locations[1] = (4,0)
			self.locations[2] = (5,0)
			self.locations[3] = (6,0)
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_O:
			self.locations[0] = (4,0)
			self.locations[1] = (5,0)
			self.locations[2] = (4,1)
			self.locations[3] = (5,1)
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_T:
			self.locations[0] = (4,0)
			self.locations[1] = (5,0)
			self.locations[2] = (6,0)
			self.locations[3] = (5,1)
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_L:
			self.locations[0] = (4,0)
			self.locations[1] = (5,0)
			self.locations[2] = (6,0)
			self.locations[3] = (4,1)
			self.tile_type = TILE_TYPE_LZ
		elif self.piece_type == PIECE_TYPE_J:
			self.locations[0] = (4,0)
			self.locations[1] = (5,0)
			self.locations[2] = (6,0)
			self.locations[3] = (6,1)
			self.tile_type = TILE_TYPE_JS
		elif self.piece_type == PIECE_TYPE_Z:
			self.locations[0] = (4,0)
			self.locations[1] = (5,0)
			self.locations[2] = (5,1)
			self.locations[3] = (6,1)
			self.tile_type = TILE_TYPE_LZ
		elif self.piece_type == PIECE_TYPE_S:
			self.locations[0] = (5,0)
			self.locations[1] = (6,0)
			self.locations[2] = (4,1)
			self.locations[3] = (5,1)
			self.tile_type = TILE_TYPE_JS


	def move(self, direction = DIRECTION_DOWN):
		if direction == DIRECTION_DOWN:
			for index, location in enumerate(self.locations):
				self.locations[index] = (location[0],location[1]+1)
		elif direction == DIRECTION_LEFT:
			for index, location in enumerate(self.locations):
				self.locations[index] = (location[0]-1,location[1])
		elif direction == DIRECTION_RIGHT:
			for index, location in enumerate(self.locations):
				self.locations[index] = (location[0]+1,location[1])