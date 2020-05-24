import lib.Globals as Globals
import lib.Constants as Constants
import copy
import pygame
from threading import Lock


class SerializableEvent:
    def __init__(self, event):
        self.type = event.type
        self.key = event.key if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP else None


class PlayerInput:
    def __init__(self):
        self.events = []
        self.new_game = False
        self.starting_level = 0
        self.player_count = 1

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return bool(self.events) or self.new_game

    def add_event(self, event):
        if event.type in (pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT):
            self.events.append(SerializableEvent(event))

    def start_game(self):
        self.new_game = True

    def set_starting_level(self, starting_level):
        self.starting_level = starting_level

    def set_player_count(self, player_count):
        self.player_count = player_count


class GameState:
    def __init__(self):
        self.tile_size =  (4 * Globals.PLAYER_COUNT) + 6
        self.board_width = Globals.BOARD_WIDTH
        self.board = []
        self.players = []
        self.current_level = 0
        self.score = 0


class Connection:
    def __init__(self):
        self.inputs = []
        self.state = GameState()
        self.lock = Lock()

    def set_input(self, player_input):
        self.input = copy.deepcopy(player_input)

    def add_input(self, player_input):
        if player_input:
            self.inputs.append(copy.deepcopy(player_input))

    def get_input(self):
        return self.inputs.pop(0) if self.inputs else PlayerInput()

    def set_state(self, state):
        self.state = copy.deepcopy(state)

    def get_state(self):
        return self.state
