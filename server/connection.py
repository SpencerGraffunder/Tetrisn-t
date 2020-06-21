import copy
import pygame
from threading import Lock
from common.player_input import *


class Connection:
    def __init__(self):
        self.inputs = []
        self.state = None
        self.lock = Lock()

    def get_input(self):
        return self.inputs.pop(0) if self.inputs else PlayerInput(None)

    def set_state(self, state):
        self.state = copy.deepcopy(state)


