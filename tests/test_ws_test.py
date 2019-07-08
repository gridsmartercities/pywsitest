import unittest
from unittest.mock import patch, MagicMock
from src.ws_test import WSTest
import asyncio


class WSTestTests(unittest.TestCase):


    def test_create_ws_test_with_uri(self):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        self.assertEqual(uri, ws_tester.uri)

    def test_add_key_value_query_parameter(self):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        key = "example"
        value = 123

        ws_tester.with_query_parameter(key, value)

        self.assertEqual(value, ws_tester.query_parameters[key])

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    async def test_websocket_connect(self, mock_ssl, mock_socket):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        await ws_tester.run()

        mock_socket.assert_called_once_with((uri, mock_ssl))


        