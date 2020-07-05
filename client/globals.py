from common.player_input import ControlType
import pygame
from client.constants import *
import configparser
from server.server import Server
import json
import os

# Globals are all stored as globals, there's a Config class which has functions to load and save settings.
# Loading sets the globals, saving saves the globals.

default_keybindings = {0: {pygame.K_a: ControlType.LEFT,
                           pygame.K_d: ControlType.RIGHT,
                           pygame.K_s: ControlType.DOWN,
                           pygame.K_q: ControlType.CCW,
                           pygame.K_e: ControlType.CW,
                           pygame.K_ESCAPE: ControlType.PAUSE},
                       1: {pygame.K_f: ControlType.LEFT,
                           pygame.K_h: ControlType.RIGHT,
                           pygame.K_g: ControlType.DOWN,
                           pygame.K_r: ControlType.CCW,
                           pygame.K_y: ControlType.CW,
                           pygame.K_ESCAPE: ControlType.PAUSE},
                       2: {pygame.K_j: ControlType.LEFT,
                           pygame.K_l: ControlType.RIGHT,
                           pygame.K_k: ControlType.DOWN,
                           pygame.K_u: ControlType.CCW,
                           pygame.K_o: ControlType.CW,
                           pygame.K_ESCAPE: ControlType.PAUSE}
                       }

# Number of players
local_player_count = 1
player_count = 1

# Score to be passed to game over state
end_score = None

# The graphics surfaces that will be drawn for each of the different tile types
tile_surfaces = {}

# Size of the board tiles on the screen in pixels
tile_size = None

tick_rate = 60

# Window dimensions in pixels
window_height = None
window_width = None

keybindings = None


class Config:
    def __init__(self):
        self.settings = configparser.ConfigParser()

    # load_settings loads the settings from config.ini, and saves the current settings to it if the file's corrupt
    def load_settings(self):
        global window_height
        global window_width
        global keybindings

        try:
            self.settings.read('config.ini')
        except:
            print('Error reading config.ini')
            self.create_default_file()
            return

        ####################################################
        # LOAD ALL VARIABLES HERE
        ####################################################
        try:
            window_height = int(self.settings.get('main', 'window_height'))
            window_width = (((4 * MAX_PLAYER_COUNT) + 18) * window_height) // 20

            loading_dict = {}
            for player_number, player_controls in json.loads(self.settings.get('main', 'keybindings')).items():
                loading_dict[int(player_number)] = {}
                for button, enum in player_controls.items():
                    loading_dict[int(player_number)][int(button)] = ControlType(enum)
            keybindings = loading_dict
        except:
            if os.path.isfile('config.ini'):
                print('Can\'t read config file. Try deleting and restarting the game.')
            else:
                self.create_default_file()

    def save_settings(self):
        try:
            self.settings.set('main', 'window_height', str(window_height))

            dumping_dict = {}
            for player_number, player_controls in keybindings.items():
                dumping_dict[player_number] = {}
                for button, enum in player_controls.items():
                    dumping_dict[player_number][button] = enum.value
            self.settings.set('main', 'keybindings', json.dumps(dumping_dict))

            fp = open('config.ini', 'w')
            self.settings.write(fp)
            fp.close()
            print('config.ini saved')
        except:
            print('Failed to save settings to config.ini')
            self.create_default_file()
            return

    def create_default_file(self):
        print('Making settings default and creating new config.ini file')

        try:
            os.remove('config.ini')
        except:
            pass

        self.settings.add_section('main')

        ####################################################
        # SET ALL DEFAULTS HERE
        ####################################################
        self.settings.set('main', 'window_height', str(700))

        dumping_dict = {}
        for player_number, player_controls in default_keybindings.items():
            dumping_dict[player_number] = {}
            for button, enum in player_controls.items():
                dumping_dict[player_number][button] = enum.value
        self.settings.set('main', 'keybindings', json.dumps(dumping_dict))

        fp = open('config.ini', 'w')
        self.settings.write(fp)
        fp.close()
        print('config.ini created')
        self.load_settings()

server = Server()

config = Config()
config.load_settings()
config.save_settings()
