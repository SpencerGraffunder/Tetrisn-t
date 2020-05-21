from States import *
import pygame
from Constants import *
from Text import *
import pdb
import Globals

class Menu(States):

	def __init__(self):
		States.__init__(self)
		self.menu_state = PLAYER_NUMBER_MENU_STATE
		self.next = 'game'

	def do_event(self, event):
	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				# ESC pressed
				self.quit = True
				return
		
			if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
			
				# Set the player count based on the key pressed
				Globals.PLAYER_COUNT = int(pygame.key.name(event.key))
				
				# Bound the player count (can add more later)
				if Globals.PLAYER_COUNT != 1:
					Globals.PLAYER_COUNT = 2
					
				# Move to the next menu state
				self.menu_state = LEVEL_SELECT_MENU_STATE
					
			elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
					
				try:
					# Get the value of the key pressed and cast to int
					key_pressed = int(pygame.key.name(event.key))
				except ValueError:
					# Value was not an int so just return and wait for a real int
					return
				
				Globals.CURRENT_LEVEL = key_pressed

				# add 10 if LSHIFT is pressed
				keys = pygame.key.get_pressed()
				if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
					Globals.CURRENT_LEVEL += 10
				# start the game
				Globals.GAME_JUST_STARTED = True
				# go to the menu where the user chooses the number of players after quitting the game
				self.menu_state = PLAYER_NUMBER_MENU_STATE

				self.done = True
				

	def update(self, screen, dt):
		self.draw(screen)


	def draw(self, screen):
		screen.fill((150, 150, 150))
		title_string = 'TETRISN\'T'
		subtitle_string = 'not a tetris game'

		if self.menu_state == PLAYER_NUMBER_MENU_STATE: # player number select
			text.draw(screen, title_string, 'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//4), (0, 160, 0))
			text.draw(screen, subtitle_string, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2//4), (0, 120, 0))

			single_string = 'Press 1 for single player'
			multi_string = 'Press 0 for multi player'
			text.draw(screen, single_string, 'SMALL', (Globals.WINDOW_WIDTH*1//4, Globals.WINDOW_HEIGHT*3//4), (150, 0, 0))
			text.draw(screen, multi_string, 'SMALL', (Globals.WINDOW_WIDTH*3//4, Globals.WINDOW_HEIGHT*3//4), (150, 0, 0))
		elif self.menu_state == LEVEL_SELECT_MENU_STATE: # level select
			text.draw(screen, title_string, 'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//4), (0, 160, 0))
			text.draw(screen, subtitle_string, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2//4), (0, 120, 0))

			level_string_line1 = 'Enter the starting level\'s number'
			level_string_line2 = 'Hold LSHIFT to add 10'
			text.draw(screen, level_string_line1, 'SMALL', (Globals.WINDOW_WIDTH*1//2, Globals.WINDOW_HEIGHT*3//4 - 15), (150, 0, 0))
			text.draw(screen, level_string_line2, 'SMALL', (Globals.WINDOW_WIDTH*1//2, Globals.WINDOW_HEIGHT*3//4 + 15), (150, 0, 0))