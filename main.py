from threading import Thread
from client.client import Client
from server.server import Server



if __name__ == '__main__':
    server = Server()
    server.start()
    client = Client()
    client.start()

