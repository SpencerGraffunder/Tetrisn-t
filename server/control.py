import server.globals as g
import pygame

class Control:
    def __init__(self):
        self.done = False
        self.clock = pygame.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def flip_state(self):
        self.state.done = False
        self.state_name = self.state.next
        self.state = self.state_dict[self.state_name]

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(g.tick_rate)/1000.0
            print(self.state)
            self.update(delta_time)