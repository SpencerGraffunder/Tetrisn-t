import copy
import pygame
from threading import Lock
from common.player_input import *

class Connection:
    def __init__(self):
        self.inputs = []
        self.state = None
        self.lock = Lock()

    def add_input(self, player_input):
        if player_input:
            self.inputs.append(copy.deepcopy(player_input))

    def get_state(self):
        return self.state


connection = Connection()
