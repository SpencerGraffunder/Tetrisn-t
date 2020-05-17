from Constants import *

class Tile:
	
	def __init__(self, tile_type = TILE_TYPE_BLANK, is_active = False):
		self.tile_type = None
		self.is_active = False
		self.tile_type = tile_type
		self.is_active = is_active