import copy
import pygame
from threading import Lock
from common.player_input import *


class GameState:
    def __init__(self):
        self.board_width = 10
        self.board_height = 20
        self.board = []
        self.players = []
        self.current_level = 0
        self.score = 0
        self.game_over = False
        self.player_count = 0

    def set_player_count(self, player_count):
        self.player_count = player_count


class Connection:
    def __init__(self):
        self.inputs = []
        self.state = GameState()
        self.lock = Lock()

    def add_input(self, player_input):
        if player_input:
            self.inputs.append(copy.deepcopy(player_input))

    def get_input(self):
        return self.inputs.pop(0) if self.inputs else PlayerInput(None)

    def set_state(self, state):
        self.state = copy.deepcopy(state)

    def get_state(self):
        return self.state


connection = Connection()
