from States import *
import pygame
from Constants import *
from Text import *

class Game_Over(States):

	def __init__(self):
		States.__init__(self)
		self.next = 'game over'

	def do_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.done = True
			if event.key == pygame.K_ESCAPE:
				self.quit = True

	def update(self, screen, dt):
		self.draw(screen)

	def draw(self, screen):
		screen.fill((100,255,100))
		text.draw(screen, 'Game Over', 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (128, 50, 0))
