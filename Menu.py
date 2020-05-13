from States import *
import pygame
from tetrisnt_enums import *
from Text import *

class Menu(States):

	def __init__(self):
		States.__init__(self)
		self.menu_state = PLAYER_NUMBER_MENU_STATE
		self.next = 'game'

	def do_event(self, event):
		if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					States.player_count = 1
					self.menu_state = LEVEL_SELECT_MENU_STATE
				if event.key == pygame.K_0:
					States.player_count = 2
					self.menu_state = LEVEL_SELECT_MENU_STATE
				if event.key == pygame.K_ESCAPE:
					self.quit = True
		elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_0:
					States.current_level = 2
					self.done = True
					States.just_started = True
				if event.key == pygame.K_1:
					States.current_level = 1
					self.done = True
					States.just_started = True
				if event.key == pygame.K_ESCAPE:
					self.quit = True

	def update(self, screen, dt):
		self.draw(screen)


	def draw(self, screen):
		screen.fill((150, 150, 150))
		title_string = 'TETRISN\'T'

		if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
			text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))

			subtitle_string = 'not a tetris game'
			text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

			single_string = 'Press 1 for single player'
			multi_string = 'Press 0 for multi player'
			text.draw(screen, single_string, 'SMALL', (WINDOW_WIDTH*1//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
			text.draw(screen, multi_string, 'SMALL', (WINDOW_WIDTH*3//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
		elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
			text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))

			subtitle_string = 'not a tetris game'
			text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

			single_string = 'Press 1 for single player'
			multi_string = 'Press 0 for multi player'
			text.draw(screen, single_string, 'SMALL', (WINDOW_WIDTH*1//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
			text.draw(screen, multi_string, 'SMALL', (WINDOW_WIDTH*3//4, WINDOW_HEIGHT*3//4), (150, 0, 0))