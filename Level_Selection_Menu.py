from States import *
import pygame
from Constants import *
from Text import *
import pdb
import Globals

class Level_Selection_Menu(States):

    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        

    def do_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC pressed
                self.switch('main menu')
                return

            try:
                # Get the value of the key pressed and cast to int
                Globals.CURRENT_LEVEL = int(pygame.key.name(event.key))
            except ValueError:
                # Value was not an int so just return and wait for a real int
                return

            # add 10 if LSHIFT is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                Globals.CURRENT_LEVEL += 10

            # start the game
            Globals.GAME_JUST_STARTED = True

            self.done = True


    def update(self, dt):
        pass


    def draw(self, screen):
        screen.fill((150, 150, 150))
        
        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'
        level_string_line1 = 'Enter the starting level\'s number'
        level_string_line2 = 'Hold LSHIFT to add 10'

        text.draw(screen, title_string,    'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//4),   (0, 160, 0))
        text.draw(screen, subtitle_string, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2//4), (0, 120, 0))
        text.draw(screen, level_string_line1, 'SMALL', (Globals.WINDOW_WIDTH*1//2, Globals.WINDOW_HEIGHT*3//4 - 15), (150, 0, 0))
        text.draw(screen, level_string_line2, 'SMALL', (Globals.WINDOW_WIDTH*1//2, Globals.WINDOW_HEIGHT*3//4 + 15), (150, 0, 0))