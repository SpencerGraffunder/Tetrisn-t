from States import *
import pygame
import Globals
from Constants import *
from Text import *

class Game_Over(States):

    def __init__(self):
        States.__init__(self)
        

    def do_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                self.switch('main menu')
                
                
    def update(self, dt):
        pass
        

    def draw(self, screen):
        screen.fill((100,255,100))
        text.draw(screen, 'Game Over', 'LARGE', (Globals.WINDOW_WIDTH//2, Globals.WINDOW_HEIGHT//2), (128, 50, 0))