import asyncio
import json
import ssl
import websockets
from .ws_response import WSResponse
from .ws_message import WSMessage


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
        with_parameter(key, value):
            Adds a parameter and returns the WSTest
        with_response(response: WSResponse):
            Adds an expected response and returns the WSTest
        with_message(message: WSMessage):
            Adds a message to send and returns the WSTest
        with_response_timeout(timeout: float):
            Sets the response timeout in seconds and returns the WSTest
        with_message_timeout(timeout: float):
            Sets the message timeout in seconds and returns the WSTest
        with_test_timeout(timeout: float):
            Sets the overall test timeout in seconds and returns the WSTest
        async run():
            Runs the websocket tester with the current configuration
        is_complete():
            Checks whether the test has completed and returns the result as a bool

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

        assert ws_tester.is_complete()
    """

    def __init__(self, uri):
        """
        Parameters:
            uri (str): The uri of the websocket api
        """
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
        """
        Adds a key/value pair to the parameters dictionary
        Parameters are query parameters used to connect to the websocket

        Parameters:
            key (obj): The key of the parameter
            value (obj, optional): The value of the parameter

        Returns:
            (WSTest): The WSTest instance with_parameter was called on
        """
        self.parameters[key] = value
        return self

    def with_response(self, response: WSResponse):
        """
        Adds a response to the expected responses list

        Parameters:
            response (WSResponse): An expected response

        Returns:
            (WSTest): The WSTest instance with_response was called on
        """
        self.expected_responses.append(response)
        return self

    def with_message(self, message: WSMessage):
        """
        Adds a message to the messages list

        Parameters:
            message (WSMessage): A message to send to the websocket

        Returns:
            (WSTest): The WSTest instance with_message was called on
        """
        self.messages.append(message)
        return self

    def with_response_timeout(self, timeout: float):
        """
        Sets the response timeout in seconds

        Parameters:
            timeout (float): The time to wait for a response in seconds

        Returns:
            (WSTest): The WSTest instance with_response_timeout was called on
        """
        self.response_timeout = timeout
        return self

    def with_message_timeout(self, timeout: float):
        """
        Sets the message timeout in seconds

        Parameters:
            timeout (float): The time to wait for a message to send in seconds

        Returns:
            (WSTest): The WSTest instance with_message_timeout was called on
        """
        self.message_timeout = timeout
        return self

    def with_test_timeout(self, timeout: float):
        """
        Sets the test timeout in seconds

        Parameters:
            timeout (float): The time to wait for the test to finish in seconds

        Returns:
            (WSTest): The WSTest instance with_test_timeout was called on
        """
        self.test_timeout = timeout
        return self

    async def run(self):
        """
        Runs the integration tests
        Sends any messages to the websocket
        Receives any responses from the websocket

        Raises:
            asyncio.TimeoutError: If the test/sending/receiving fails to finish within the time limit
        """
        websocket = await websockets.connect(self._get_connection_string(), ssl=ssl.SSLContext())
        try:
            # Run the receive and send methods async with a timeout
            await asyncio.wait_for(self._runner(websocket), timeout=self.test_timeout)
        finally:
            await websocket.close()

    async def _runner(self, websocket):
        await asyncio.gather(self._receive(websocket), self._send(websocket))

    async def _receive(self, websocket):
        # iterate while there are still expected responses that haven't been received yet
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
        # wss://example.com?first=123&second=456
        connection_string = self.uri
        if self.parameters:
            connection_string += "?"
        for key in self.parameters:
            connection_string += str(key) + "=" + str(self.parameters[key]) + "&"
        return connection_string.strip("&")

    def is_complete(self):
        """
        Checks whether the test has finished running

        Returns:
            (bool): Value to indicate whether the test has finished
        """
        return not self.expected_responses and not self.messages
