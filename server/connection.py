import copy
import pygame
from threading import Lock
from common.player_input import PlayerInput
import common.messages as m


class Connection:
    def __init__(self):
        self.player_inputs = []
        self.new_client = 0
        self.state = None
        self.lock = Lock()

    def add_game_state(self, game_state):
        m.client_inbox.append(m.GameStateMessage(game_state))

    def add_player_numbers(self, player_numbers):
        m.client_inbox.append(m.PlayerNumbersMessage(player_numbers))

    def get_new_client_local_players(self):
        self.__read_messages()
        return self.new_client_local_players

    def get_player_input(self):
        self.__read_messages()
        return self.player_inputs.pop(0) if self.player_inputs else PlayerInput(None)

    def __read_messages(self):
        while m.server_inbox:
            msg = m.server_inbox.pop(0)
            if msg.type == m.Message.Type.NEW_CLIENT:
                self.new_client_local_players = msg.data['new_client']
            elif msg.type == m.Message.Type.PLAYER_INPUT:
                self.player_inputs.append(msg.data['player_inputs'])
