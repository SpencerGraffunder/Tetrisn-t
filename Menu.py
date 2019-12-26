from States import *
import pygame
from tetrisnt_enums import *

class Menu(States):

	def __init__(self):
		States.__init__(self)
		self.next = 'game'
		self.font = pygame.font.Font('freesansbold.ttf', 72)
		self.text = self.font.render('Tetrisn\'t', True, (0, 128, 0))
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (window_width//2, window_height//2)

	def do_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.done = True
			if event.key == pygame.K_ESCAPE:
				self.quit = True

	def update(self, screen, dt):
		self.draw(screen)

	def draw(self, screen):
		screen.fill((100,255,0))
		screen.blit(self.text, self.text_rect)