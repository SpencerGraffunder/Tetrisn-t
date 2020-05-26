import pygame
from lib.states.States import *
import sys
import os
from lib.components.Tile import *  # Import like this to avoid having to do Tile. before everything
from lib.components.Piece import *
from lib.components.Player import *
import random
from collections import deque
import lib.Globals as Globals
from lib.Constants import *
from lib.components.Text import *
from lib.Connection import GameState

class Connecting(States):
    def __init__(self):
        States.__init__(self)
        self.reset()

    def reset(self):
        self.done = False

    def update(self, dt):
        while Globals.connection.inputs:
            player_input = Globals.connection.get_input()
            if player_input.new_game:
                self.switch('server game')
                Globals.connection.add_input(player_input)
                break

    def draw(self, screen):
        pass
