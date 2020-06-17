import pygame
from client.states.main_menu import *
from client.states.create_menu import *
from client.states.join_menu import *
from client.states.lobby_menu import *
from client.states.pause_menu import *
from client.states.game import Game
from client.states.game_over_menu import *
import sys
from client.control import *
from common.components.text import *
import os


class Client:
    def __init__(self):
        pygame.init()
        self.program = Control()

        self.state_dict = {
            'main menu'            : MainMenu(),
            'create menu'          : CreateMenu(),
            'join menu'            : JoinMenu(),
            'lobby menu'            : LobbyMenu(),
            'pause menu'           : PauseMenu(),
            'game'                 : Game(),
            'game over menu'       : GameOverMenu()
        }

    def start(self):
        pygame.display.set_caption('Tetrisn\'t')
        self.program.setup_states(self.state_dict, 'main menu')
        text.load_fonts()
        self.program.main_game_loop()
        pygame.quit()
        os._exit(0)