import copy
import pygame
import json
import socket
from threading import Lock
from common.player_input import PlayerInput
import common.messages as m
import server.constants as c
import server.globals as g

class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.player_numbers = []

    def get_msg(self):
        # read from network
        data = self.conn.recv(4096)
        if not data:
            return None

        return json.loads(data.dedoce('utf-8'))

    def send_msg(self, msg):
        json_msg = json.dumps(msg).encode('utf-8')
        self.conn.sendall(json_msg)


class Connection:
    def __init__(self):
        self.player_inputs = []
        self.new_client = 0
        self.state = None
        self.lock = Lock()
        self.clients = []

    def add_game_state(self, game_state):
        game_state_msg = m.GameStateMessage(game_state)
        for client in self.clients:
            client.send_msg(game_state_msg)

    def add_player_numbers(self, player_numbers):
        m.client_inbox.append(m.PlayerNumbersMessage(player_numbers))

    def get_player_input(self):
        self.__read_messages()
        return self.player_inputs.pop(0) if self.player_inputs else PlayerInput(None)

    def read_client_messages(self):
        for client in self.clients:
            msg = client.get_msg()
            if msg.type == m.Message.Type.NEW_CLIENT and not client.player_numbers:

                local_players = msg.data['new_client']
                new_player_range = range(g.state.player_count,
                                         g.state.player_count + local_players)
                client.player_numbers = [i for i in new_player_range]
                client.send_msg(m.PlayerNumbersMessage(client.player_numbers))

            elif msg.type == m.Message.Type.PLAYER_INPUT:
                self.player_inputs.append(msg.data['player_inputs'])

    def check_for_new_clients(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((c.SERVER_ADDR, c.SERVER_ADDR))
                s.listen()
                s.settimeout(0.01)
                conn, addr = s.accept()
                self.clients.append(Client(conn, addr))

            except Exception as e:
                # Error accepting new client
                print(str(e))
                return
