import pygame
from Constants import *
import os
import sys
import Globals

# Example
# text.draw(screen, score_str1, 'SMALL', ((WINDOW_WIDTH) - (4 * TILE_SIZE), (BOARD_HEIGHT - 3) * TILE_SIZE), (0, 128, 0))

class Text:

	def __init__(self):
		pass
		
	
	def load_fonts(self):
		LARGE_FONT_SIZE	 = Globals.WINDOW_HEIGHT//5
		MEDIUM_FONT_SIZE = Globals.WINDOW_HEIGHT//10
		SMALL_FONT_SIZE	 = Globals.WINDOW_HEIGHT//20
		
		if getattr(sys, 'frozen', False):
			wd = sys._MEIPASS
		else:
			wd = ''
		
		self.fonts = {
			'LARGE'	 : pygame.font.Font(os.path.join(wd, 'resources/munro-small.ttf'), LARGE_FONT_SIZE),
			'MEDIUM' : pygame.font.Font(os.path.join(wd, 'resources/munro-small.ttf'), MEDIUM_FONT_SIZE),
			'SMALL'	 : pygame.font.Font(os.path.join(wd, 'resources/munro-small.ttf'), SMALL_FONT_SIZE)
		}


	def draw(self, screen, text_str, size, pos, color):
		text			 = self.fonts[size].render(text_str, True, color)
		text_rect		 = text.get_rect()
		text_rect.center = pos
		screen.blit(text, text_rect)

text = Text()