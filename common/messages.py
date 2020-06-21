from enum import Enum

class Message:
    class Type(Enum):
        NEW_CLIENT = 1
        PLAYER_NUMBERS = 2
        GAME_STATE = 3
        PLAYER_INPUT = 4

    def __init__(self, type_):
        self.type = type_


class NewClientMessage(Message):
    def __init__(self, local_player_count):
        self.type = self.Type.NEW_CLIENT
        self.data = {"new_client": local_player_count}

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