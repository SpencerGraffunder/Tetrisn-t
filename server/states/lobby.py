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
        #g.connection.check_for_new_players()
        while g.connection.player_inputs:
            player_input = g.connection.get_player_input()

            if player_input.is_ready:
                g.state.players[player_input.player_number].is_ready = True

        if all([p.is_ready for p in g.state.players]):
            g.state.game_started = True
            g.connection.add_game_state(g.state)
            self.switch('game')
