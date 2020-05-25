from States import *
import pygame
from Constants import *
from Text import *
import pdb
import Globals

class Main_Menu(States):

    def __init__(self):
        States.__init__(self)
        self.next = 'level selection menu'


    def do_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC pressed
                self.quit = True
                return


            try:
                # Set the player count based on the key pressed
                Globals.PLAYER_COUNT = int(pygame.key.name(event.key))
            except ValueError:
                # Value was not an int so just return and wait for a real int
                return

            # Bound the player count (can add more later)
            if Globals.PLAYER_COUNT != 1:
                Globals.PLAYER_COUNT = 2

            Globals.BOARD_WIDTH = (4 * Globals.PLAYER_COUNT) + 6
            TILE_SIZE = min(Globals.WINDOW_WIDTH,Globals.WINDOW_HEIGHT) // max(Globals.BOARD_WIDTH,Globals.BOARD_HEIGHT)

            # Move to the player selection state
            self.done = True


    def update(self, dt):
        pass
        

    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'

        text.draw(screen, title_string,    'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//4),   (0, 160, 0))
        text.draw(screen, subtitle_string, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2//4), (0, 120, 0))

        single_string = 'Press 1 for single player'
        multi_string  = 'Press 0 for multi player'
        text.draw(screen, single_string, 'SMALL', (Globals.WINDOW_WIDTH*1//4, Globals.WINDOW_HEIGHT*3//4), (150, 0, 0))
        text.draw(screen, multi_string,  'SMALL', (Globals.WINDOW_WIDTH*3//4, Globals.WINDOW_HEIGHT*3//4), (150, 0, 0))