import pygame
import client.globals as g
from common.components.text import *
from client.constants import *


class Control:
    def __init__(self):
        self.done = False
        self.screen = pygame.display.set_mode((g.window_width, g.window_height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.state_dict = None
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        for event in pygame.event.get(pygame.VIDEORESIZE):
            g.window_height = event.h
            g.window_width = (((4*MAX_PLAYER_COUNT)+18)*g.window_height)//20
            text.load_fonts()
            self.screen = pygame.display.set_mode((g.window_width, g.window_height), pygame.RESIZABLE)
        self.state.update()

    def draw(self):
        self.state.draw(self.screen)

    def flip_state(self):
        self.state.done = False
        self.state_name = self.state.next
        self.state = self.state_dict[self.state_name]

    def main_game_loop(self):
        while not self.done:
            self.update()
            self.draw()
