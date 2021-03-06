from client.states.state import *
import pygame
import client.globals as g
from common.components.text import *


class GameOverMenu(State):

    def __init__(self):
        State.__init__(self)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    self.switch('main menu')

    def draw(self, screen):
        screen.fill((100, 255, 100))
        text.draw(screen, 'Game Over', 'LARGE', (g.window_width//2, g.window_height//3), (128, 50, 0))
        text.draw(screen, 'Score: ' + str(g.end_score), 'LARGE', (g.window_width//2, g.window_height*2//3), (128, 60, 20))
        pygame.display.update()

