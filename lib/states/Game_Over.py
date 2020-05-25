from lib.states.States import *
import pygame
import lib.Globals as Globals
from lib.Constants import *
from lib.components.Text import *

class Game_Over(States):

    def __init__(self):
        States.__init__(self)
        self.next = 'main menu'
                
    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    self.done = True

    def draw(self, screen):
        screen.fill((100,255,100))
        text.draw(screen, 'Game Over', 'LARGE', (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (128, 50, 0))
        pygame.display.update()

