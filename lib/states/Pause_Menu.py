from lib.states.States import *
import pygame
from lib.Constants import *
from lib.components.Text import *
from lib.Connection import PlayerInput
import pdb
import lib.Globals

class Pause_Menu(States):

    def __init__(self):
        States.__init__(self)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go to the main menu
                    self.switch('main menu')

                elif event.key == pygame.K_SPACE:
                    # Go back to the game
                    player_input = PlayerInput()
                    player_input.resume_game()
                    Globals.connection.add_input(player_input)
                    self.switch('client game')

                self.done = True

    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'Pause'
        space_string = 'Press SPACE to continue'
        esc_string = 'Press ESC for main menu'

        text.draw(screen, title_string, 'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//4),   (0, 160, 0))
        text.draw(screen, space_string, 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*2//4), (0, 120, 0))
        text.draw(screen, esc_string  , 'SMALL', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT*3//4), (0, 120, 0))
        pygame.display.update()
