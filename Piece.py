from tetrisnt_enums import *
import pdb
import sys
from copy import copy

class Piece:

	def __init__(self, piece_type):
	
		self.piece_type = 0
		self.tile_type = 0
		self.rotation = 0
		self.locations = [(0,0),(0,0),(0,0),(0,0)] # col,row
		self.piece_type = piece_type
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


	def move(self, direction = DIRECTION_DOWN, locations = None):
	
		if locations == None:
			locations = self.locations
			
		if direction == DIRECTION_DOWN:
			for index, location in enumerate(locations):
				locations[index] = (location[0],location[1]+1)
		elif direction == DIRECTION_LEFT:
			for index, location in enumerate(locations):
				locations[index] = (location[0]-1,location[1])
		elif direction == DIRECTION_RIGHT:
			for index, location in enumerate(locations):
				locations[index] = (location[0]+1,location[1])
				
				
	def can_move(self, board, direction):
	
		test_locations = copy(self.locations)
		
		self.move(direction, test_locations)
				
		for location in test_locations:
			if location[1] >= len(board) or location[0] < 0 or location[0] >= len(board[0]):
				return False
			if board[location[1]][location[0]].tile_type != TILE_TYPE_BLANK:
				return False
		
		return True

		
	def rotate(self, rotation_direction, locations = None, rotation = None):
	
		if locations == None:
			locations = self.locations
		if rotation == None:
			rotation = self.rotation
	
		if self.piece_type == PIECE_TYPE_O: # for the meme
			pass
		elif self.piece_type == PIECE_TYPE_Z: # the special case
			if rotation in [0,180]:
				pivot = copy(locations[1])
				locations[0] = (pivot[0]+1,pivot[1]-1)
				locations[1] = (pivot[0]+1,pivot[1])
				locations[2] = pivot
				locations[3] = (pivot[0],pivot[1]+1)
				rotation = (rotation+90) % 360
			elif rotation in [90,270]:
				pivot = copy(locations[2])
				locations[0] = (pivot[0]-1,pivot[1])
				locations[1] = pivot
				locations[2] = (pivot[0],pivot[1]+1)
				locations[3] = (pivot[0]+1,pivot[1]+1)
				rotation = (rotation+90) % 360
		elif self.piece_type == PIECE_TYPE_I or self.piece_type == PIECE_TYPE_S: # the two-rotation-position pieces that aren't special
			if self.piece_type == PIECE_TYPE_I:
				pivot = locations[2]
				if rotation in [0,180]:
					turn = TURN_CW # turn to vertical
				else:
					turn = TURN_CCW # turn to horizontal
			elif self.piece_type == PIECE_TYPE_S:
				pivot = copy(locations[0])
				if rotation in [0,180]:
					turn = TURN_CCW # turn to vertical
				else:
					turn = TURN_CW # turn to horizontal
			if turn == TURN_CW:
				# General rotate CW:
				for i, location in enumerate(locations):
					locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
				rotation = (rotation+90) % 360
			elif turn == TURN_CCW:
				# General rotate CCW:
				for i, location in enumerate(locations):
					locations[i] = ((location[1]-pivot[1])+pivot[0],(pivot[0]-location[0])+pivot[1])
				rotation = (rotation-90) % 360
		elif self.piece_type == PIECE_TYPE_T or self.piece_type == PIECE_TYPE_L or self.piece_type == PIECE_TYPE_J: # the four-rotation-position pieces
			pivot = copy(locations[1])
			if rotation_direction == ROTATION_CW:
				# General rotate CW:
				for i, location in enumerate(locations):
					locations[i] = ((pivot[1]-location[1])+pivot[0],(location[0]-pivot[0])+pivot[1])
				rotation = (rotation+90) % 360
			elif rotation_direction == ROTATION_CCW:
				# General rotate CCW:
				for i, location in enumerate(locations):
					locations[i] = ((location[1]-pivot[1])+pivot[0],(pivot[0]-location[0])+pivot[1])
				rotation = (rotation-90) % 360
				
				
	def can_rotate(self, board, rotation_direction):
	
		test_locations = copy(self.locations)
		test_rotation = copy(self.rotation)
		
		self.rotate(rotation_direction, test_locations, test_rotation)
				
		for location in test_locations:
			if location[1] >= len(board) or location[0] < 0 or location[0] >= len(board[0]):
				return False
			if board[location[1]][location[0]].tile_type != TILE_TYPE_BLANK:
				return False
		
		return True