import pygame

class Text:

	def __init__(self):
		pass
		
	
	def load_fonts(self):
		LARGE_FONT_SIZE  = 90
		MEDIUM_FONT_SIZE = 50
		SMALL_FONT_SIZE  = 20
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