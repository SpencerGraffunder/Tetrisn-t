import copy
import pygame
from threading import Lock
from common.player_input import *
from enum import Enum


class GameState:
    class Progress(Enum):
        LOBBY = 1
        PLAY = 2
        PAUSE = 3
        OVER = 4

    def __init__(self):
        self.board_width = 10
        self.board_height = 20
        self.board = []
        self.players = []
        self.current_level = 0
        self.score = 0
        self.player_count = 0
        self.progress = GameState.Progress.LOBBY

    @property
    def player_count(self):
        return len(self.players)

