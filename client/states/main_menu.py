from client.states.state import *
import pygame
from common.components.text import *
import pdb
from client.globals import *
from client.constants import *


class MainMenu(State):
    def __init__(self):
        State.__init__(self)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                g.window_height = event.h
                g.window_width = (((4*MAX_PLAYER_COUNT)+18)*g.window_height)//20

            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC pressed
                    self.quit = True
                    g.save_settings()
                    return

                try:
                    # Set the player count based on the key pressed
                    g.local_player_count = int(pygame.key.name(event.key))
                except ValueError:
                    # Value was not an int so just return and wait for a real int
                    return

                # Bound the player count (can add more later)
                if g.local_player_count not in [1, 2]:
                    return

                if g.local_player_count == 1:
                    self.switch('create menu')
                elif g.local_player_count == 2:
                    self.switch('join menu')

    def draw(self, screen):
        screen.fill((150, 150, 150))
        title_string = 'TETRISN\'T'
        subtitle_string = 'not a tetris game'

        text.draw(screen, title_string,    'LARGE', (g.window_width//2, g.window_height//4),   (0, 160, 0))
        text.draw(screen, subtitle_string, 'SMALL', (g.window_width//2, g.window_height*2//4), (0, 120, 0))

        player_count_string = 'Press 1 to create a game'
        text.draw(screen, player_count_string, 'SMALL', (g.window_width//2, g.window_height*3//4), (150, 0, 0))

        player_count_string = 'Press 2 to join a game'
        text.draw(screen, player_count_string, 'SMALL', (g.window_width//2, g.window_height*3.3//4), (150, 0, 0))
        pygame.display.update()
