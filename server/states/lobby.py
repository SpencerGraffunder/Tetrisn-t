from server.states.state import *
from common.connection import connection


class Lobby(State):
    def __init__(self):
        State.__init__(self)
        self.reset()

    def reset(self):
        self.done = False

    def update(self):
        while connection.inputs:
            player_input = connection.get_input()
            if player_input.new_game:
                self.switch('game')
                connection.add_input(player_input)
                break
