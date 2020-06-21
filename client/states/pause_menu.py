from client.states.state import *
import pygame
from common.components.text import *
from common.player_input import PlayerInput
from client.connection import connection
import pdb
import client.globals as g


class PauseMenu(State):

    def __init__(self):
        State.__init__(self)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go to the main menu
                    self.switch('main menu')

                elif event.key == pygame.K_SPACE:
                    # Go back to the game
                    player_input = PlayerInput(None)
                    player_input.resume_game()
                    connection.add_player_input(player_input)
                    self.switch('game')

    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'Pause'
        space_string = 'Press SPACE to continue'
        esc_string = 'Press ESC for main menu'

        text.draw(screen, title_string, 'LARGE', (g.window_width//2, g.window_height//4),   (0, 160, 0))
        text.draw(screen, space_string, 'SMALL', (g.window_width//2, g.window_height*2//4), (0, 120, 0))
        text.draw(screen, esc_string  , 'SMALL', (g.window_width//2, g.window_height*3//4), (0, 120, 0))
        pygame.display.update()
