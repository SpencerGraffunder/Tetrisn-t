import pygame
import pdb
from lib.Constants import *
from copy import copy
from lib.states.States import *
from threading import Thread
from lib.states.Main_Menu import *
from lib.states.Level_Selection_Menu import *
from lib.states.Pause_Menu import *
from lib.states.ClientGame import ClientGame
from lib.states.Game_Over import *
import sys
from lib.states.Control import *
from lib.components.Text import *
import os


class Client:
    def __init__(self):
        pygame.init()
        self.program = Control()

        self.state_dict = {
            'main menu'            : Main_Menu(),
            'level selection menu' : Level_Selection_Menu(),
            'pause menu'           : Pause_Menu(),
            'client game'          : ClientGame(),
            'game over'            : Game_Over()
        }

    def start(self):
        pygame.display.set_caption('Tetrisn\'t')
        self.program.setup_states(self.state_dict, 'main menu')
        text.load_fonts()
        self.program.main_game_loop()
        pygame.quit()
        os._exit(0)