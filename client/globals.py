from common.player_input import ControlType
import pygame
from client.constants import *
import configparser


class Settings:
    def __init__(self):
        self.settings = configparser.ConfigParser()

        # Number of players
        self.local_player_count = 1
        self.player_count = 1

        self.tick_rate = 60

        # Window dimensions in pixels
        self.window_height = None
        self.window_width = None

        # Size of the board tiles on the screen in pixels
        self.tile_size = None

        self.keybindings = {0: {pygame.K_a: ControlType.LEFT,
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

        # The graphics surfaces that will be drawn for each of the different tile types
        self.tile_surfaces = {}

    def load_settings(self):
        self.settings.read('config.ini')
        if not self.settings.has_section('main'):
            self.settings.add_section('main')

            ####################################################
            # SET ALL DEFAULTS HERE
            ####################################################
            self.settings.set('main', 'window_height', str(700))

        ####################################################
        # LOAD ALL VARIABLES HERE
        ####################################################
        self.window_height = int(self.settings.get('main', 'window_height'))
        self.window_width = (((4 * MAX_PLAYER_COUNT) + 18) * self.window_height) // 20

    def save_settings(self):
        self.settings.set('main', 'window_height', str(self.window_height))
        fp = open('config.ini', 'w')
        self.settings.write(fp)
        fp.close()


g = Settings()
g.load_settings()

# # Number of players
# local_player_count = 1
# player_count = 1
#
# tick_rate = 60
#
# # Window dimensions in pixels
# window_height = g.window_height
# window_width = (((4 * MAX_PLAYER_COUNT) + 18) * window_height) // 20
#
# # Size of the board tiles on the screen in pixels
# tile_size = None
#
# keybindings = {0: {pygame.K_a: ControlType.LEFT,
#                    pygame.K_d: ControlType.RIGHT,
#                    pygame.K_s: ControlType.DOWN,
#                    pygame.K_q: ControlType.CCW,
#                    pygame.K_e: ControlType.CW,
#                    pygame.K_ESCAPE: ControlType.PAUSE},
#                1: {pygame.K_f: ControlType.LEFT,
#                    pygame.K_h: ControlType.RIGHT,
#                    pygame.K_g: ControlType.DOWN,
#                    pygame.K_r: ControlType.CCW,
#                    pygame.K_y: ControlType.CW,
#                    pygame.K_ESCAPE: ControlType.PAUSE},
#                2: {pygame.K_j: ControlType.LEFT,
#                    pygame.K_l: ControlType.RIGHT,
#                    pygame.K_k: ControlType.DOWN,
#                    pygame.K_u: ControlType.CCW,
#                    pygame.K_o: ControlType.CW,
#                    pygame.K_ESCAPE: ControlType.PAUSE}
#                }
#
# # The graphics surfaces that will be drawn for each of the different tile types
# tile_surfaces = {}
