from client.states.state import *
import pygame
from common.components.text import *
import pdb
import client.globals as g


class MainMenu(State):
    def __init__(self):
        State.__init__(self)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC pressed
                    self.quit = True
                    return

                try:
                    # Set the player count based on the key pressed
                    g.local_player_count = int(pygame.key.name(event.key))
                except ValueError:
                    # Value was not an int so just return and wait for a real int
                    return

                # Bound the player count (can add more later)
                if g.local_player_count != 1:
                    g.local_player_count = 4

                # Move to the player selection state
                self.switch('level selection menu')

    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'

        text.draw(screen, title_string,    'LARGE', (g.window_width//2, g.window_height//4),   (0, 160, 0))
        text.draw(screen, subtitle_string, 'SMALL', (g.window_width//2, g.window_height*2//4), (0, 120, 0))

        single_string = 'Press 1 for single player'
        multi_string  = 'Press 0 for multi player'
        text.draw(screen, single_string, 'SMALL', (g.window_width*1//4, g.window_height*3//4), (150, 0, 0))
        text.draw(screen, multi_string,  'SMALL', (g.window_width*3//4, g.window_height*3//4), (150, 0, 0))
        pygame.display.update()
