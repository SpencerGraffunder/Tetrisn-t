from server.states.state import *
from server.connection import Connection
import server.globals as g


class Lobby(State):
    def __init__(self):
        State.__init__(self)
        self.reset()

    def reset(self):
        self.done = False

    def update(self):
        # Check for new connections?
        connection.check_for_new_players()
        while connection.inputs:
            player_input = connection.get_input()

            if player_input.is_ready:
                self.state.players[player_input.player_number].is_ready = True

        if all([p.is_ready for p in self.state.players]):
            self.state.game_started = True
            connection.set_state(self.state)
            self.switch('game')
