
import socket
import random
from itertools import count
from time import sleep

from src.log import get_logger


logger = get_logger(__name__)


operations = ['GET', 'POST', 'PUT', 'DELETE']
client_id = count(0, 1)


class Client:

    def __init__(self):
        self.client_id = next(client_id)

    def connect(self, host, port):

        logger.info(f'Client {self.client_id} - Initializing connection')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                logger.info(f'Client {self.client_id} - Connected')

                while True:
                    sleep(random.randint(2, 4))
                    try:
                        op = random.choices(operations, [3, 3, 2, 1], k=1)[0]
                        data = bytes(op, encoding='utf8')
                        s.sendall(data)
                        logger.info(f'Client {self.client_id} - Requested {data}')

                        res = s.recv(1024)
                        logger.info(f'Client {self.client_id} - Received {res}')
                    except Exception as e:
                        logger.error(f'Client {self.client_id} - Error while trasfering data: {e}')

            except Exception as e:
                logger.error(f'Client {self.client_id} - Connection not established: {e}')
