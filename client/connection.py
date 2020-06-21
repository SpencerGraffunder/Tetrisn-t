import copy
import pygame
from threading import Lock
from common.player_input import *
import common.messages as m

class Connection:
    def __init__(self):
        self.inputs = []
        self.game_state = None
        self.lock = Lock()
        self.player_numbers = []

    def add_player_input(self, player_input):
        m.server_inbox.append(m.PlayerInputMessage(player_input))

    def get_game_state(self):
        self.__read_messages()
        return self.game_state

    def get_player_numbers(self):
        self.__read_messages()
        return self.player_numbers

    # clears the current client inbox, parsing all messages
    def __read_messages(self):
        while m.client_inbox:
            msg = m.client_inbox.pop(0)
            if msg.type == m.Message.Type.PLAYER_NUMBERS:
                self.player_numbers = msg.data['player_numbers']
            elif msg.type == m.Message.Type.GAME_STATE:
                self.game_state = msg.data['game_state']


connection = Connection()
