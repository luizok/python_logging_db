import sys
import socket
from threading import Thread
from time import sleep
import random

from src.log import get_logger, init
from src.log.dbloggers import loggable


logger = get_logger(__name__)


def on_new_client(conn, client_addr):

    try:
        while True:
            data = conn.recv(1024)
            logger.info(f'Server - received {data}')
            if data:
                res = random.choices([0, 1], weights=[1, 3], k=1)[0]
                if res == 1:
                    logger.info(f'Server - Sending back {res}')
                else:
                    logger.error('Server - Error processing data')

                sleep(random.randint(1, 2))
                conn.sendall(bytes(str(res), encoding='utf8'))
    finally:
        conn.close()


@loggable
class Server:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.logger.info('Server - Initializing server')
        try:
            self._sock.bind((self._host, self._port))
            self._sock.listen()
        except OSError as e:
            self.logger.error(f'Server - {e}')
            return

        while True:
            self.logger.info('Server - Waiting for a connection')
            try:
                conn, client_addr = self._sock.accept()
                t = Thread(target=on_new_client, args=(conn, client_addr))
                t.start()
            except Exception as e:
                self.logger.error(f'Server - {e}')
            except KeyboardInterrupt:
                self.logger.error('Server - closed')
                return
