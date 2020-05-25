from States import *
import pygame
from Constants import *
from Text import *
import pdb
import Globals

class Level_Selection_Menu(States):

    def __init__(self):
        States.__init__(self)
        self.level_selection = 0


    def do_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC pressed
                self.switch('main menu')
                return
            elif event.key == pygame.K_UP:
                if self.level_selection < 29:
                    self.level_selection += 1
            elif event.key == pygame.K_DOWN:
                if self.level_selection > 0:
                    self.level_selection -= 1
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                Globals.GAME_JUST_STARTED = True
                Globals.CURRENT_LEVEL = self.level_selection
                self.switch('game')


    def update(self, dt):
        pass


    def draw(self, screen):
        screen.fill((150, 150, 150))

        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'
        instruction_line1 = 'press UP or DOWN to change starting level'
        instruction_line2 = 'press SPACE to start'
        selection_string = str(self.level_selection)

        text.draw(screen, title_string,      'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT   //4),  (0, 160, 0))
        text.draw(screen, subtitle_string,   'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2 //4),  (0, 120, 0))
        text.draw(screen, instruction_line1, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*5 //8),  (150, 0, 0))
        text.draw(screen, instruction_line2, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*11//16), (150, 0, 0))
        text.draw(screen, selection_string,  'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*13//16), (150, 0, 0))