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
		if self.piece_type == previous_piece:
			self.piece_type = random.choice([PIECE_TYPE_I,PIECE_TYPE_O,PIECE_TYPE_T,PIECE_TYPE_L,PIECE_TYPE_J,PIECE_TYPE_Z,PIECE_TYPE_S])
		previous_piece = self.piece_type
		self.rotation = 0
		if self.piece_type == PIECE_TYPE_I:
			self.locations[0] = (3,0) # [-][-][-][-] | [-][-][0][-]
			self.locations[1] = (4,0) # [-][-][-][-] | [-][-][1][-]
			self.locations[2] = (5,0) # [0][1][2][3] | [-][-][2][-]
			self.locations[3] = (6,0) # [-][-][-][-] | [-][-][3][-]
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_O:
			self.locations[0] = (4,0) #
			self.locations[1] = (5,0) # [0][1]
			self.locations[2] = (4,1) # [2][3]
			self.locations[3] = (5,1) #
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_T:
			self.locations[0] = (4,0) # [-][-][-] | [-][0][-] | [-][3][-] | [-][2][-]
			self.locations[1] = (5,0) # [0][1][2] | [3][1][-] | [2][1][0] | [-][1][3]
			self.locations[2] = (6,0) # [-][3][-] | [-][2][-] | [-][-][-] | [-][0][-]
			self.locations[3] = (5,1) #			  |			  |			  |
			self.tile_type = TILE_TYPE_IOT
		elif self.piece_type == PIECE_TYPE_L:
			self.locations[0] = (4,0) # [-][-][-] | [3][0][-] | [-][-][3] | [-][2][-]
			self.locations[1] = (5,0) # [0][1][2] | [-][1][-] | [2][1][0] | [-][1][-]
			self.locations[2] = (6,0) # [3][-][-] | [-][2][-] | [-][-][-] | [-][0][3]
			self.locations[3] = (4,1) # 		  |		      |		      |
			self.tile_type = TILE_TYPE_LZ
		elif self.piece_type == PIECE_TYPE_J:
			self.locations[0] = (4,0) #	[-][-][-] | [-][0][-] | [3][-][-] | [-][2][3]
			self.locations[1] = (5,0) # [0][1][2] | [-][1][-] | [2][1][0] | [-][1][-]
			self.locations[2] = (6,0) # [-][-][3] | [3][2][-] | [-][-][-] | [-][0][-]
			self.locations[3] = (6,1) #			  |           |           |
			self.tile_type = TILE_TYPE_JS
		elif self.piece_type == PIECE_TYPE_Z:
			self.locations[0] = (4,0) # [-][-][-] | [-][-][0]
			self.locations[1] = (5,0) # [0][1][-] | [-][2][1]
			self.locations[2] = (5,1) # [-][2][3] | [-][3][-]
			self.locations[3] = (6,1) #			  |
			self.tile_type = TILE_TYPE_LZ
		elif self.piece_type == PIECE_TYPE_S:
			self.locations[0] = (5,0) # [-][-][-] | [-][1][-]
			self.locations[1] = (6,0) # [-][0][1] | [-][0][3]
			self.locations[2] = (4,1) # [2][3][-] | [-][-][2]
			self.locations[3] = (5,1) # 		  |
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

	def rotate(self, rotation_direction):
		if self.piece_type == PIECE_TYPE_O: # for the meme
			pass
		elif self.piece_type == PIECE_TYPE_Z: # the special case
			if self.rotation in [0,180]:
				pivot = self.locations[1]
				self.locations[0] = (pivot[0]+1,pivot[1]-1)
				self.locations[1] = (pivot[0]+1,pivot[1])
				self.locations[2] = pivot
				self.locations[3] = (pivot[0],pivot[1]+1)
			elif self.rotation in [90,270]:
				pivot = self.locations[2]
				self.locations[0] = (pivot[0]-1,pivot[1])
				self.locations[1] = pivot
				self.locations[2] = (pivot[0],pivot[1]+1)
				self.locations[3] = (pivot[0]+1,pivot[1]+1)
		elif self.piece_type == PIECE_TYPE_I or self.piece_type == PIECE_TYPE_S: # the two-rotation-position pieces that aren't special
			if self.piece_type == PIECE_TYPE_I:
				pivot = self.locations[2]
				if self.rotation in [0,180]:
					turn = TURN_CW # turn to vertical
				else:
					turn = TURN_CCW # turn to horizontal
			elif self.piece_type == PIECE_TYPE_S:
				pivot = self.locations[0]
				if self.rotation in [0,180]:
					turn = TURN_CCW # turn to vertical
				else:
					turn = TURN_CW # turn to horizontal
			if turn == TURN_CW:
				# General rotate CW:
				for position in self.locations:
					pos_copy = position
					position[0] = (pivot[1]-pos_copy[1])+pivot[0]
					position[1] = (pos_copy[1]-pivot[1])+pivot[1]
					self.rotation = (self.rotation+90) % 360
			elif turn == TURN_CCW:
				# General rotate CCW:
				for position in self.locations:
					pos_copy = position
					position[0] = (pos_copy[1]-pivot[1])+pivot[1]
					position[1] = (pivot[1]-pos_copy[1])+pivot[1]
					self.rotation = (self.rotation-90) % 360
		elif self.piece_type == PIECE_TYPE_T or self.piece_type == PIECE_TYPE_L or self.piece_type == PIECE_TYPE_J: # the four-rotation-position pieces
			pivot = self.position[1]
			if rotation_direction == ROTATION_CW:
				# General rotate CW:
				for position in self.locations:
					pos_copy = position
					position[0] = (pivot[1]-pos_copy[1])+pivot[0]
					position[1] = (pos_copy[1]-pivot[1])+pivot[1]
					self.rotation = (self.rotation+90) % 360
			elif rotation_direction == ROTATION_CCW:
				# General rotate CCW:
				for position in self.locations:
					pos_copy = position
					position[0] = (pos_copy[1]-pivot[1])+pivot[1]
					position[1] = (pivot[1]-pos_copy[1])+pivot[1]
					self.rotation = (self.rotation-90) % 360