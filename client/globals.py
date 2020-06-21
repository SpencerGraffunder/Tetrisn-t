from common.player_input import ControlType
import pygame
from client.constants import *
import configparser
from server.server import Server
import json
import os

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


class Settings:
    def __init__(self):
        self.settings = configparser.ConfigParser()

        # Number of players
        self.local_player_count = 1
        self.player_count = 1

        # The graphics surfaces that will be drawn for each of the different tile types
        self.tile_surfaces = {}

        # Size of the board tiles on the screen in pixels
        self.tile_size = None

        self.tick_rate = 60

        # Window dimensions in pixels
        self.window_height = None
        self.window_width = None

        self.keybindings = None

    # load_settings loads the settings from config.ini, and saves the current settings to it if the file's corrupt
    def load_settings(self):
        try:
            self.settings.read('config.ini')
        except:
            print("Error reading config.ini")
            self.new_default_file()
            return

        ####################################################
        # LOAD ALL VARIABLES HERE
        ####################################################
        try:
            self.window_height = int(self.settings.get('main', 'window_height'))
        except:
            self.new_default_file()
            return
        self.window_width = (((4 * MAX_PLAYER_COUNT) + 18) * self.window_height) // 20

        try:
            loading_dict = {}
            for player_number, player_controls in json.loads(self.settings.get('main', 'keybindings')).items():
                loading_dict[int(player_number)] = {}
                for button, enum in player_controls.items():
                    loading_dict[int(player_number)][int(button)] = ControlType(enum)
            self.keybindings = loading_dict
        except:
            self.new_default_file()
            return

    def save_settings(self):
        try:
            self.settings.set('main', 'window_height', str(self.window_height))

            dumping_dict = {}
            for player_number, player_controls in self.keybindings.items():
                dumping_dict[player_number] = {}
                for button, enum in player_controls.items():
                    dumping_dict[player_number][button] = enum.value
            self.settings.set('main', 'keybindings', json.dumps(dumping_dict))

            fp = open('config.ini', 'w')
            self.settings.write(fp)
            fp.close()
            print("config.ini modified (unless program just started)")
        except:
            print("Failed to save settings to config.ini")
            self.new_default_file()
            return

    def new_default_file(self):
        print("Making settings default and creating new config.ini file")

        try:
            os.remove('config.ini')
        except:
            pass

        if not self.settings.has_section('main'):
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
        print("config.ini created")
        self.load_settings()


g = Settings()
g.load_settings()
g.save_settings()

server = Server()
