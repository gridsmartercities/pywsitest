import asyncio
import unittest
from unittest.mock import patch, MagicMock
from src.ws_test import WSTest


def syncify(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper


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

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_connect(self, mock_ssl, mock_websockets):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        mock_websockets.connect.assert_called_once_with(uri, ssl=ssl_context)
        mock_socket.close.assert_called_once()

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_connect_with_parameters(self, mock_ssl, mock_websockets):
        uri = "wss://example.com"
        ws_tester = (
            WSTest(uri)
            .with_query_parameter("example", 123)
            .with_query_parameter("test", 456)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        expected_uri = "wss://example.com?example=123&test=456"

        mock_websockets.connect.assert_called_once_with(expected_uri, ssl=ssl_context)
        mock_socket.close.assert_called_once()
