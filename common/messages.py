from enum import Enum

class Message:
    class Type(Enum):
        PLAYER_NUMBERS = 1
        GAME_STATE = 2
        PLAYER_INPUT = 3

    def __init__(self, type_):
        self.type = type_


class PlayerNumbersMessage(Message):
    def __init__(self, player_numbers):
        self.type = self.Type.PLAYER_NUMBERS
        self.data = {"player_numbers": player_numbers}


class GameStateMessage(Message):
    def __init__(self, game_state):
        self.type = self.Type.GAME_STATE
        self.data = {"game_state": game_state}


class PlayerInputMessage(Message):
    def __init__(self, player_input):
        self.type = self.Type.PLAYER_INPUT
        self.data = {"player_input": player_input}

client_inbox = []
server_inbox = []