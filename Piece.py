from tetrisnt_enums import *
import pdb

class Piece:
	piece_type = 0
	tile_type = 0
	rotation = 0
	locations = [(0,0),(0,0),(0,0),(0,0)] # col,row

	def __init__(self, piece_type = PIECE_TYPE_I):
		self.piece_type = piece_type
		self.rotation = 0
		if piece_type == PIECE_TYPE_I:
			self.locations[0] = (3,0)
			self.locations[1] = (4,0)
			self.locations[2] = (5,0)
			self.locations[3] = (6,0)
			self.tile_type = TILE_TYPE_IST

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