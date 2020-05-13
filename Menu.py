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
				if event.key == pygame.K_1 or event.key == pygame.K_KP1:
					States.player_count = 1
					self.menu_state = LEVEL_SELECT_MENU_STATE
				if event.key == pygame.K_0 or event.key == pygame.K_KP0:
					States.player_count = 2
					self.menu_state = LEVEL_SELECT_MENU_STATE
				if event.key == pygame.K_ESCAPE:
					self.quit = True
		elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_0 or event.key == pygame.K_KP0:
					States.current_level = 0
					self.done = True
					States.just_started = True
				if event.key == pygame.K_1 or event.key == pygame.K_KP1:
					States.current_level = 1
					self.done = True
					States.just_started = True
				if event.key == pygame.K_2 or event.key == pygame.K_KP2:
					States.current_level = 2
					self.done = True
					States.just_started = True
				if event.key == pygame.K_3 or event.key == pygame.K_KP3:
					States.current_level = 3
					self.done = True
					States.just_started = True
				if event.key == pygame.K_4 or event.key == pygame.K_KP4:
					States.current_level = 4
					self.done = True
					States.just_started = True
				if event.key == pygame.K_5 or event.key == pygame.K_KP5:
					States.current_level = 5
					self.done = True
					States.just_started = True
				if event.key == pygame.K_6 or event.key == pygame.K_KP6:
					States.current_level = 6
					self.done = True
					States.just_started = True
				if event.key == pygame.K_7 or event.key == pygame.K_KP7:
					States.current_level = 7
					self.done = True
					States.just_started = True
				if event.key == pygame.K_8 or event.key == pygame.K_KP8:
					States.current_level = 8
					self.done = True
					States.just_started = True
				if event.key == pygame.K_9 or event.key == pygame.K_KP9:
					States.current_level = 9
					self.done = True
					States.just_started = True
				if event.key == pygame.K_ESCAPE:
					self.quit = True

				# add 10 if LSHIFT is pressed
				keys = pygame.key.get_pressed()
				if keys[pygame.K_LSHIFT]:
					States.current_level += 10


	def update(self, screen, dt):
		self.draw(screen)


	def draw(self, screen):
		screen.fill((150, 150, 150))
		title_string = 'TETRISN\'T'
		subtitle_string = 'not a tetris game'

		if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
			text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))
			text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

			single_string = 'Press 1 for single player'
			multi_string = 'Press 0 for multi player'
			text.draw(screen, single_string, 'SMALL', (WINDOW_WIDTH*1//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
			text.draw(screen, multi_string, 'SMALL', (WINDOW_WIDTH*3//4, WINDOW_HEIGHT*3//4), (150, 0, 0))
		elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
			text.draw(screen, title_string, 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//4), (0, 160, 0))
			text.draw(screen, subtitle_string, 'SMALL', (WINDOW_WIDTH//2, WINDOW_HEIGHT*2//4), (0, 120, 0))

			level_string_line1 = 'Enter the starting level\'s number'
			level_string_line2 = 'Hold LSHIFT to add 10'
			text.draw(screen, level_string_line1, 'SMALL', (WINDOW_WIDTH*1//2, WINDOW_HEIGHT*3//4 - 15), (150, 0, 0))
			text.draw(screen, level_string_line2, 'SMALL', (WINDOW_WIDTH*1//2, WINDOW_HEIGHT*3//4 + 15), (150, 0, 0))