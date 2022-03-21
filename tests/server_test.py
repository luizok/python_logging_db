import unittest
import mock

from src.server import Server, on_new_client


class ServerTestCase(unittest.TestCase):

    @mock.patch('src.server.get_logger')
    @mock.patch('socket.socket')
    def test_init(self, socket, _):
        socket.return_value = sock_obj = mock.Mock()

        s = Server('localhost', 6669)

        self.assertEqual(s._host, 'localhost')
        self.assertEqual(s._port, 6669)
        self.assertEqual(s._sock, sock_obj)

    @mock.patch('src.server.Thread')
    @mock.patch('socket.socket')
    @mock.patch('src.server.get_logger')
    def test_start_success(self, _, socket, thread):
        socket.return_value = sock_obj = mock.Mock()
        client = ('host', 7777)
        # KeyboardInterrupt just to interrupt the endless loop
        sock_obj.accept.side_effect = [client, KeyboardInterrupt()]
        thread.return_value = thread_obj = mock.Mock()
        host, port = 'localhost', 6669

        s = Server(host, port)
        try:
            s.start()
        except KeyboardInterrupt:
            pass

        sock_obj.bind.assert_called_with((host, port))
        sock_obj.listen.called_once()
        thread.assert_called_with(target=on_new_client, args=client)
        thread_obj.start.assert_called_once()
