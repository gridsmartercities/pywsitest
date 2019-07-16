import asyncio
import json
import ssl
import websockets
from src.ws_response import WSResponse
from src.ws_message import WSMessage


class WSTest:  # noqa: pylint - too-many-instance-attributes
    """
    A class representing a websocket test runner

    Attributes:
        uri (str)
        parameters (dict)
        messages (list)
        sent_messages (list)
        expected_responses (list)
        received_responses (list)
        received_json (list)
        response_timeout (float)
        message_timeout (float)
        test_timeout (float)

    Methods:
        with_parameter
        with_response
        with_message
        with_response_timeout
        with_message_timeout
        with_test_timeout
        run
        is_complete

    Usage:
        ws_tester = (
            WSTest("wss://example.com")
            .with_parameter("Authorization", "eyJh...")
            .with_response(
                WSResponse()
            )
            .with_response(
                WSResponse()
            )
            .with_message(
                WSMessage()
            )
        )

        await ws_tester.run()

        assertTrue(ws_tester.is_complete())
    """

    def __init__(self, uri):
        self.uri = uri
        self.parameters = {}
        self.messages = []
        self.sent_messages = []
        self.expected_responses = []
        self.received_responses = []
        self.received_json = []
        self.response_timeout = 10.0
        self.message_timeout = 10.0
        self.test_timeout = 60.0

    def with_parameter(self, key, value):
        self.parameters[key] = value
        return self

    def with_response(self, response: WSResponse):
        self.expected_responses.append(response)
        return self

    def with_message(self, message: WSMessage):
        self.messages.append(message)
        return self

    def with_response_timeout(self, timeout: float):
        self.response_timeout = timeout
        return self

    def with_message_timeout(self, timeout: float):
        self.message_timeout = timeout
        return self

    def with_test_timeout(self, timeout: float):
        self.test_timeout = timeout
        return self

    async def run(self):
        websocket = await websockets.connect(self._get_connection_string(), ssl=ssl.SSLContext())
        try:
            await asyncio.wait_for(self._runner(websocket), timeout=self.test_timeout)
        finally:
            await websocket.close()

    async def _runner(self, websocket):
        await asyncio.gather(self._receive(websocket), self._send(websocket))

    async def _receive(self, websocket):
        while self.expected_responses:
            response = await asyncio.wait_for(websocket.recv(), timeout=self.response_timeout)
            await self._receive_handler(websocket, response)

    async def _receive_handler(self, websocket, response):
        self.received_json.append(response)
        parsed_response = json.loads(response)

        for expected_response in self.expected_responses:
            if expected_response.is_match(parsed_response):
                self.received_responses.append(expected_response)
                self.expected_responses.remove(expected_response)

                for message in expected_response.triggers:
                    await self._send_handler(websocket, message)

                break

    async def _send(self, websocket):
        while self.messages:
            message = self.messages.pop(0)
            await self._send_handler(websocket, message)

    async def _send_handler(self, websocket, message):
        await asyncio.wait_for(websocket.send(str(message)), timeout=self.message_timeout)
        self.sent_messages.append(message)

    def _get_connection_string(self):
        connection_string = self.uri
        if self.parameters:
            connection_string += "?"
        for key in self.parameters:
            connection_string += str(key) + "=" + str(self.parameters[key]) + "&"
        return connection_string.strip("&")

    def is_complete(self):
        return not self.expected_responses
