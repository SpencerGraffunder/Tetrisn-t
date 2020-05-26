import pdb
from lib.Constants import *
from copy import copy
from lib.states.States import *
from lib.states.ServerGame import *
from lib.states.Connecting import *
import sys
from lib.states.Control import *
from threading import Thread

class Server:
    def __init__(self):
        self.program = Control()

        self.state_dict = {
            'connecting': Connecting(),
            'server game': ServerGame(),
        }

    def start(self):
        server_thread = Thread(target=self.server_loop)
        server_thread.start()

    def server_loop(self):
        try:
            self.program.setup_states(self.state_dict, 'connecting')
            self.program.main_game_loop()
            sys.exit()
        except Exception as e:
            print(e)