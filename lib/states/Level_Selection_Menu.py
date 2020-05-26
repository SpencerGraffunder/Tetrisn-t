from lib.states.States import *
import pygame
from lib.Constants import *
from lib.components.Text import *
from lib.Connection import PlayerInput
import pdb
import client.globals as g
from lib.Connection import connection

class Level_Selection_Menu(States):

    def __init__(self):
        States.__init__(self)
        self.level_selection = 0

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC pressed
                    self.switch('main menu')
                    return

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
                    starting_level = self.level_selection

                    # start the game
                    player_input = PlayerInput()
                    player_input.start_game()
                    player_input.set_starting_level(starting_level)
                    player_input.set_player_count(g.local_player_count)
                    connection.add_input(player_input)
                    self.switch('client game')

    def draw(self, screen):
        screen.fill((150, 150, 150))

        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'
        instruction_line1 = 'press UP or DOWN to change starting level'
        instruction_line2 = 'press SPACE to start'
        selection_string = str(self.level_selection)

        text.draw(screen, title_string,      'LARGE', (g.WINDOW_WIDTH//2, g.WINDOW_HEIGHT   //4),  (0, 160, 0))
        text.draw(screen, subtitle_string,   'SMALL', (g.WINDOW_WIDTH//2, g.WINDOW_HEIGHT*2 //4),  (0, 120, 0))
        text.draw(screen, instruction_line1, 'SMALL', (g.WINDOW_WIDTH//2, g.WINDOW_HEIGHT*5 //8),  (150, 0, 0))
        text.draw(screen, instruction_line2, 'SMALL', (g.WINDOW_WIDTH//2, g.WINDOW_HEIGHT*11//16), (150, 0, 0))
        text.draw(screen, selection_string,  'LARGE', (g.WINDOW_WIDTH//2, g.WINDOW_HEIGHT*13//16), (150, 0, 0))
        pygame.display.update()
