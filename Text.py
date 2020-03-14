import pygame
from tetrisnt_enums import *

# Example
# text.draw(screen, score_str1, 'SMALL', ((WINDOW_WIDTH) - (4 * TILE_SIZE), (BOARD_HEIGHT - 3) * TILE_SIZE), (0, 128, 0))

class Text:

	def __init__(self):
		pass
		
	
	def load_fonts(self):
		LARGE_FONT_SIZE  = WINDOW_HEIGHT//5
		MEDIUM_FONT_SIZE = WINDOW_HEIGHT//10
		SMALL_FONT_SIZE  = WINDOW_HEIGHT//20
		self.fonts = {
			'LARGE'  : pygame.font.Font('munro-small.ttf', LARGE_FONT_SIZE),
			'MEDIUM' : pygame.font.Font('munro-small.ttf', MEDIUM_FONT_SIZE),
			'SMALL'  : pygame.font.Font('munro-small.ttf', SMALL_FONT_SIZE)
		}


	def draw(self, screen, text_str, size, pos, color):
		text             = self.fonts[size].render(text_str, True, color)
		text_rect        = text.get_rect()
		text_rect.center = pos
		screen.blit(text, text_rect)

text = Text()