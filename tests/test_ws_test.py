import asyncio
import json
import unittest
from unittest.mock import patch, MagicMock
from src.ws_test import WSTest
from src.ws_response import WSResponse


def syncify(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(coro(*args, **kwargs))
        loop.close()
        return response
    return wrapper


class WSTestTests(unittest.TestCase):

    def test_create_ws_test_with_uri(self):
        ws_tester = WSTest("wss://example.com")
        self.assertEqual("wss://example.com", ws_tester.uri)

    def test_add_key_value_query_parameter(self):
        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
        )

        self.assertEqual(123, ws_tester.query_parameters["example"])

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_connect(self, mock_ssl, mock_websockets):
        ws_tester = WSTest("wss://example.com")

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        mock_websockets.connect.assert_called_once_with("wss://example.com", ssl=ssl_context)
        mock_socket.close.assert_called_once()

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_connect_with_parameters(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
            .with_parameter("test", 456)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        expected_uri = "wss://example.com?example=123&test=456"

        await ws_tester.run()

        mock_websockets.connect.assert_called_once_with(expected_uri, ssl=ssl_context)
        mock_socket.close.assert_called_once()

    def test_websocket_with_expected_response(self):
        response = WSResponse().with_attribute("type")
        ws_tester = WSTest("wss://example.com").with_response(response)

        self.assertTrue(ws_tester.expected_responses)
        self.assertEqual(response, ws_tester.expected_responses[0])

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_receives_and_handles_single_response(self, mock_ssl, mock_websockets):
        response = WSResponse().with_attribute("body")

        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
            .with_response(response)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        response_json = json.dumps({"body": {}})
        future = asyncio.Future()
        future.set_result(response_json)
        mock_socket.recv = MagicMock(side_effect=[future, asyncio.Future()])

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertEqual(response, ws_tester.actual_responses[0])
        self.assertEqual(response_json, ws_tester.received_responses[0])
        self.assertTrue(ws_tester.is_complete())
        mock_socket.close.assert_called_once()

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_receives_and_handles_multiple_responses(self, mock_ssl, mock_websockets):
        first_response = WSResponse().with_attribute("body")
        second_response = WSResponse().with_attribute("type")

        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
            .with_response(first_response)
            .with_response(second_response)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        first_future = asyncio.Future()
        first_future.set_result(json.dumps({"body": {}}))
        second_future = asyncio.Future()
        second_future.set_result(json.dumps({"type": {}}))
        mock_socket.recv = MagicMock(side_effect=[second_future, first_future, asyncio.Future()])

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertEqual(2, len(ws_tester.received_responses))
        self.assertEqual(2, len(ws_tester.actual_responses))
        self.assertTrue(ws_tester.is_complete())
        mock_socket.close.assert_called_once()

    def test_websocket_receive_when_no_expected_responses(self):
        ws_tester = WSTest("wss://example.com")
        ws_tester._receive_handler(json.dumps({"body": {}}))  # noqa: pylint - protected-access

        self.assertTrue(ws_tester.received_responses)
        self.assertFalse(ws_tester.actual_responses)

    @patch("src.ws_test.websockets")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_response_timeout(self, mock_ssl, mock_websockets):
        response = WSResponse().with_attribute("body")

        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
            .with_response_timeout(0.1)
            .with_response(response)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_socket.recv = MagicMock(return_value=asyncio.Future())

        mock_websockets.connect = MagicMock(return_value=asyncio.Future())
        mock_websockets.connect.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        self.assertEqual(ws_tester.response_timeout, 0.1)
        with self.assertRaises(asyncio.TimeoutError):
            await ws_tester.run()
        mock_socket.close.assert_called_once()
