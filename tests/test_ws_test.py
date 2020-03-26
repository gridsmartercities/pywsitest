import asyncio
import json
import unittest
from unittest.mock import patch, MagicMock

from pywsitest import WSTest, WSResponse, WSMessage, WSTimeoutError


def syncify(coro):
    def wrapper(*args, **kwargs):
        response = asyncio.run(coro(*args, **kwargs))
        return response
    return wrapper


class WSTestTests(unittest.TestCase):  # noqa: pylint - too-many-public-methods

    def test_create_ws_test_with_uri(self):
        ws_tester = WSTest("wss://example.com")
        self.assertEqual("wss://example.com", ws_tester.uri)

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_whitespace_is_stripped_from_uri_on_connect(self, mock_ssl, mock_websockets):
        ws_tester = WSTest("\n wss://example.com \n")

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        mock_websockets.assert_called_once_with("wss://example.com", ssl=ssl_context)
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_whitespace_is_stripped_from_uri_with_query_parameter_on_connect(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("\n wss://example.com \n")
            .with_parameter("\n test \n", "\n example \n")
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        expected_uri = "wss://example.com?test=example"
        mock_websockets.assert_called_once_with(expected_uri, ssl=ssl_context)
        mock_socket.close.assert_called_once()

    def test_add_key_value_query_parameter(self):
        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
        )

        self.assertEqual(123, ws_tester.parameters["example"])

    def test_add_key_value_message(self):
        message = WSMessage().with_attribute("test", 123)

        ws_tester = (
            WSTest("wss://example.com")
            .with_message(message)
        )

        self.assertEqual(1, len(ws_tester.messages))
        self.assertEqual(message, ws_tester.messages[0])

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_connect(self, mock_ssl, mock_websockets):
        ws_tester = WSTest("wss://example.com")

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        mock_websockets.assert_called_once_with("wss://example.com", ssl=ssl_context)
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @syncify
    async def test_websocket_connect_unsecured(self, mock_websockets):
        ws_tester = WSTest("ws://example.com")

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        await ws_tester.run()

        mock_websockets.assert_called_once_with("ws://example.com", ssl=None)
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
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

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        expected_uri = "wss://example.com?example=123&test=456"

        await ws_tester.run()

        mock_websockets.assert_called_once_with(expected_uri, ssl=ssl_context)
        mock_socket.close.assert_called_once()

    def test_websocket_with_expected_response(self):
        response = WSResponse().with_attribute("type")
        ws_tester = WSTest("wss://example.com").with_response(response)

        self.assertTrue(ws_tester.expected_responses)
        self.assertEqual(response, ws_tester.expected_responses[0])

    @patch("websockets.connect")
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

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertEqual(response, ws_tester.received_responses[0])
        self.assertEqual(response_json, ws_tester.received_json[0])
        self.assertTrue(ws_tester.is_complete())
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
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

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertEqual(2, len(ws_tester.received_json))
        self.assertEqual(2, len(ws_tester.received_responses))
        self.assertTrue(ws_tester.is_complete())
        mock_socket.close.assert_called_once()

    @syncify
    async def test_websocket_receive_when_no_expected_responses(self):
        ws_tester = WSTest("wss://example.com")
        mock_socket = MagicMock()
        await ws_tester._receive_handler(mock_socket, json.dumps({"body": {}}))  # noqa: pylint - protected-access

        self.assertTrue(ws_tester.received_json)
        self.assertFalse(ws_tester.received_responses)

    @patch("websockets.connect")
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

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        self.assertEqual(ws_tester.response_timeout, 0.1)
        with self.assertRaises(WSTimeoutError):
            await ws_tester.run()
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_response_timeout_with_received_response_logging_enabled(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_response_timeout(0.1)
            .with_received_response_logging()
            .with_response(
                WSResponse()
                .with_attribute("message", "hello")
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        first_future = asyncio.Future()
        first_future.set_result(json.dumps({"message": "bye"}))

        mock_socket.recv = MagicMock(side_effect=[first_future, asyncio.Future()])

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        with self.assertRaises(WSTimeoutError) as ex:
            await ws_tester.run()

        expected_error = (
            "Timed out waiting for responses:\n{\"message\": \"hello\"}\n" +
            "Received responses:\n{\"message\": \"bye\"}"
        )
        self.assertEqual(expected_error, str(ex.exception))

        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_response_timeout_with_received_response_logging_disabled(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_response_timeout(0.1)
            .with_response(
                WSResponse()
                .with_attribute("message", "hello")
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        first_future = asyncio.Future()
        first_future.set_result(json.dumps({"message": "bye"}))

        mock_socket.recv = MagicMock(side_effect=[first_future, asyncio.Future()])

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        with self.assertRaises(WSTimeoutError) as ex:
            await ws_tester.run()

        expected_error = "Timed out waiting for responses:\n{\"message\": \"hello\"}"
        self.assertEqual(expected_error, str(ex.exception))

        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_message_timeout(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_message_timeout(0.1)
            .with_message(
                WSMessage()
                .with_attribute("test", 123)
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_socket.send = MagicMock(return_value=asyncio.Future())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        self.assertEqual(ws_tester.message_timeout, 0.1)
        with self.assertRaises(WSTimeoutError):
            await ws_tester.run()
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_test_timeout(self, mock_ssl, mock_websockets):
        response = WSResponse().with_attribute("body")

        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("example", 123)
            .with_test_timeout(0.1)
            .with_response(response)
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        mock_socket.recv = MagicMock(return_value=asyncio.Future())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        self.assertEqual(ws_tester.test_timeout, 0.1)
        with self.assertRaises(WSTimeoutError):
            await ws_tester.run()
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_test_send_single_message(self, mock_ssl, mock_websockets):
        message = WSMessage().with_attribute("test", 123)
        ws_tester = WSTest("wss://example.com").with_message(message)

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        future = asyncio.Future()
        mock_socket.send = MagicMock(return_value=future)
        future.set_result({})

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertFalse(ws_tester.messages)
        self.assertEqual(1, len(ws_tester.sent_messages))
        mock_socket.send.assert_called_once_with("{\"test\": 123}")
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_test_receive_response_with_trigger(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_response(
                WSResponse()
                .with_attribute("type")
                .with_trigger(
                    WSMessage()
                    .with_attribute("test", 123)
                )
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        send_future = asyncio.Future()
        send_future.set_result({})
        mock_socket.send = MagicMock(return_value=send_future)

        receive_future = asyncio.Future()
        receive_future.set_result(json.dumps({"type": {}}))
        mock_socket.recv = MagicMock(side_effect=[receive_future, asyncio.Future()])

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertTrue(ws_tester.is_complete())
        mock_socket.send.assert_called_once_with("{\"test\": 123}")
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_test_receive_response_with_resolved_trigger(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_response(
                WSResponse()
                .with_attribute("type")
                .with_trigger(
                    WSMessage()
                    .with_attribute("test", "${type}")
                )
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        send_future = asyncio.Future()
        send_future.set_result({})
        mock_socket.send = MagicMock(return_value=send_future)

        receive_future = asyncio.Future()
        receive_future.set_result(json.dumps({"type": "Hello, world!"}))
        mock_socket.recv = MagicMock(side_effect=[receive_future, asyncio.Future()])

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertTrue(ws_tester.is_complete())
        mock_socket.send.assert_called_once_with("{\"test\": \"Hello, world!\"}")
        mock_socket.close.assert_called_once()

    @patch("websockets.connect")
    @patch("ssl.SSLContext")
    @syncify
    async def test_websocket_test_receive_response_with_unresolved_trigger(self, mock_ssl, mock_websockets):
        ws_tester = (
            WSTest("wss://example.com")
            .with_response(
                WSResponse()
                .with_attribute("type")
                .with_trigger(
                    WSMessage()
                    .with_attribute("test", "${body}")
                )
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        send_future = asyncio.Future()
        send_future.set_result({})
        mock_socket.send = MagicMock(return_value=send_future)

        receive_future = asyncio.Future()
        receive_future.set_result(json.dumps({"type": "Hello, world!"}))
        mock_socket.recv = MagicMock(side_effect=[receive_future, asyncio.Future()])

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        ssl_context = MagicMock()
        mock_ssl.return_value = ssl_context

        await ws_tester.run()

        self.assertTrue(ws_tester.is_complete())
        mock_socket.send.assert_called_once_with("{\"test\": \"${body}\"}")
        mock_socket.close.assert_called_once()

    @patch("time.sleep")
    @patch("websockets.connect")
    @syncify
    async def test_websocket_senfing_message_with_delay(self, mock_websockets, mock_sleep):
        ws_tester = (
            WSTest("ws://example.com")
            .with_message(
                WSMessage()
                .with_attribute("test", 123)
                .with_delay(1)
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        send_future = asyncio.Future()
        send_future.set_result({})
        mock_socket.send = MagicMock(return_value=send_future)

        mock_socket.recv = MagicMock(return_value=asyncio.Future())
        mock_socket.recv.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        await ws_tester.run()

        self.assertTrue(ws_tester.is_complete())
        mock_socket.send.assert_called_once_with("{\"test\": 123}")
        mock_sleep.assert_called_once_with(1)
        mock_socket.close.assert_called_once()

    @patch("time.sleep")
    @patch("websockets.connect")
    @syncify
    async def test_websocket_senfing_message_with_no_delay(self, mock_websockets, mock_sleep):
        ws_tester = (
            WSTest("ws://example.com")
            .with_message(
                WSMessage()
                .with_attribute("test", 123)
            )
        )

        mock_socket = MagicMock()
        mock_socket.close = MagicMock(return_value=asyncio.Future())
        mock_socket.close.return_value.set_result(MagicMock())

        send_future = asyncio.Future()
        send_future.set_result({})
        mock_socket.send = MagicMock(return_value=send_future)

        mock_socket.recv = MagicMock(return_value=asyncio.Future())
        mock_socket.recv.return_value.set_result(MagicMock())

        mock_websockets.return_value = asyncio.Future()
        mock_websockets.return_value.set_result(mock_socket)

        await ws_tester.run()

        self.assertTrue(ws_tester.is_complete())
        mock_socket.send.assert_called_once_with("{\"test\": 123}")
        mock_sleep.assert_not_called()
        mock_socket.close.assert_called_once()
