from server.states.game import *
from server.states.lobby import *
import sys
from server.control import *
from threading import Thread


class Server:
    def __init__(self):
        self.program = Control()
        self.state_dict = {
            'lobby': Lobby(),
            'game': Game(),
        }

    def start(self):
        server_thread = Thread(target=self.server_loop)
        server_thread.start()

    def server_loop(self):
        try:
            self.program.setup_states(self.state_dict, 'lobby')
            self.program.main_game_loop()
            sys.exit()
        except Exception as e:
            print(e)
