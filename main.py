from threading import Thread

from src.server import Server
from src.client import Client


def init_server(host, port):

    s = Server(host, port)
    s.start()


def init_client(host, port):

    c = Client()
    c.connect(host, port)


if __name__ == '__main__':

    host = 'localhost'
    port = 2222

    s = Thread(target=init_server, args=(host, port))
    s.start()

    for i in range(4):
        c = Thread(target=init_client, args=(host, port))
        c.start()
