import asyncio
import json
import ssl

from requests.exceptions import ConnectTimeout, ReadTimeout
import websockets
from websockets.client import WebSocketClientProtocol

from .ws_message import WSMessage
from .ws_response import WSResponse
from .ws_timeout_error import WSTimeoutError
from .rest_request import RestRequest


class WSTest:  # noqa: pylint - too-many-instance-attributes
    """
    A class representing a websocket test runner

    Attributes:
        uri (str)
        parameters (dict)
        messages (list)
        requests (list)
        sent_messages (list)
        sent_requests (list)
        expected_responses (list)
        received_responses (list)
        received_json (list)
        received_request_responses (list)
        response_timeout (float)
        message_timeout (float)
        request_timeout (float)
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
        with_request_timeout(timeout: float):
            Sets the request timeout in seconds and returns the WSTest
        with_test_timeout(timeout: float):
            Sets the overall test timeout in seconds and returns the WSTest
        with_received_response_logging():
            Enables websocket received response logging and returns the WSTest
        with_request(request: RestRequest):
            Adds a rest request and returns the WSTest
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

    def __init__(self, uri: str):
        """
        Parameters:
            uri (str): The uri of the websocket api
        """
        self.uri = uri
        self.parameters = {}
        self.headers = {}
        self.messages = []
        self.requests = []
        self.sent_messages = []
        self.sent_requests = []
        self.expected_responses = []
        self.received_responses = []
        self.received_json = []
        self.received_request_responses = []
        self.response_timeout = 10.0
        self.message_timeout = 10.0
        self.request_timeout = 10.0
        self.test_timeout = 60.0
        self.log_responses_on_error = False

    def with_parameter(self, key: str, value: object) -> "WSTest":
        """
        Adds a key/value pair to the parameters dictionary
        Parameters are query parameters used to connect to the websocket

        Parameters:
            key (str): The key of the parameter
            value (obj, optional): The value of the parameter

        Returns:
            (WSTest): The WSTest instance with_parameter was called on
        """
        self.parameters[key] = value
        return self

    def with_header(self, key: str, value: object) -> "WSTest":
        """
        Adds a key/value pair to the headers dictionary
        Headers are passed to the websockets connect method

        Parameters:
            key (str): The key/name of the header
            value (obj): The value of the header

        Returns:
            (WSTest): The WSTest instance with_header was called on
        """
        self.headers[key] = value
        return self

    def with_response(self, response: WSResponse) -> "WSTest":
        """
        Adds a response to the expected responses list

        Parameters:
            response (WSResponse): An expected response

        Returns:
            (WSTest): The WSTest instance with_response was called on
        """
        self.expected_responses.append(response)
        return self

    def with_message(self, message: WSMessage) -> "WSTest":
        """
        Adds a message to the messages list

        Parameters:
            message (WSMessage): A message to send to the websocket

        Returns:
            (WSTest): The WSTest instance with_message was called on
        """
        self.messages.append(message)
        return self

    def with_response_timeout(self, timeout: float) -> "WSTest":
        """
        Sets the response timeout in seconds

        Parameters:
            timeout (float): The time to wait for a response in seconds

        Returns:
            (WSTest): The WSTest instance with_response_timeout was called on
        """
        self.response_timeout = timeout
        return self

    def with_message_timeout(self, timeout: float) -> "WSTest":
        """
        Sets the message timeout in seconds

        Parameters:
            timeout (float): The time to wait for a message to send in seconds

        Returns:
            (WSTest): The WSTest instance with_message_timeout was called on
        """
        self.message_timeout = timeout
        return self

    def with_request_timeout(self, timeout: float) -> "WSTest":
        """
        Sets the rest request timeout in seconds

        Parameters:
            timeout (float): The time to wait for a request response in seconds

        Returns:
            (WSTest): The WSTest instance with_request_timeout was called on
        """
        self.request_timeout = timeout
        return self

    def with_test_timeout(self, timeout: float) -> "WSTest":
        """
        Sets the test timeout in seconds

        Parameters:
            timeout (float): The time to wait for the test to finish in seconds

        Returns:
            (WSTest): The WSTest instance with_test_timeout was called on
        """
        self.test_timeout = timeout
        return self

    def with_received_response_logging(self) -> "WSTest":
        """
        Enables received response logging when an exception is thrown

        Returns:
            (WSTest): The WSTest instance set_log_responses_on_error was called on
        """
        self.log_responses_on_error = True
        return self

    def with_request(self, request: RestRequest) -> "WSTest":
        """
        Sets Rest request on a websocket object

        Parameters:
            request (RestRequest): The request object with all relevant data for rest request execution

        Returns:
            (WSTest): The WSTest instance with_request was called on
        """
        self.requests.append(request)
        return self

    # pylint:disable=no-member
    async def run(self):
        """
        Runs the integration tests
        Sends any messages to the websocket
        Receives any responses from the websocket

        Raises:
            WSTimeoutError: If the test/sending/receiving fails to finish within the time limit
        """
        kwargs = {}
        connection_string = self._get_connection_string()

        # add ssl if using wss
        if connection_string.startswith("wss://"):
            kwargs["ssl"] = ssl.SSLContext()

        # add headers if headers are set
        if self.headers:
            kwargs["extra_headers"] = self.headers

        websocket = await websockets.connect(connection_string, **kwargs)

        try:
            # Run the receive and send methods async with a timeout
            await asyncio.wait_for(self._runner(websocket), timeout=self.test_timeout)
        except asyncio.TimeoutError as ex:
            raise WSTimeoutError("Timed out waiting for test to finish") from ex
        finally:
            await websocket.close()

    async def _runner(self, websocket: WebSocketClientProtocol):
        await asyncio.gather(self._receive(websocket), self._send(websocket), self._request())

    async def _receive(self, websocket: WebSocketClientProtocol):
        # iterate while there are still expected responses that haven't been received yet
        while self.expected_responses:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=self.response_timeout)
                await self._receive_handler(websocket, response)
            except asyncio.TimeoutError as ex:
                error_message = self._get_receive_error_message()
                raise WSTimeoutError(error_message) from ex

    async def _receive_handler(self, websocket: WebSocketClientProtocol, response: str):
        self.received_json.append(response)
        parsed_response = json.loads(response)

        for expected_response in self.expected_responses:
            if expected_response.is_match(parsed_response):
                self.received_responses.append(expected_response)
                self.expected_responses.remove(expected_response)
                await self._trigger_handler(websocket, expected_response, parsed_response)
                break

    async def _trigger_handler(self, websocket: WebSocketClientProtocol, response: WSResponse, raw_response: dict):
        for message in response.triggers:
            message = message.resolve(raw_response)
            await self._send_handler(websocket, message)

    async def _send(self, websocket: WebSocketClientProtocol):
        while self.messages:
            message = self.messages.pop(0)
            await self._send_handler(websocket, message)

    async def _send_handler(self, websocket: WebSocketClientProtocol, message: WSMessage):
        try:
            if message.delay:
                await asyncio.sleep(message.delay)
            await asyncio.wait_for(websocket.send(str(message)), timeout=self.message_timeout)
            self.sent_messages.append(message)
        except asyncio.TimeoutError as ex:
            error_message = "Timed out trying to send message:\n" + str(message)
            raise WSTimeoutError(error_message) from ex

    async def _request(self):
        while self.requests:
            request = self.requests.pop(0)
            await self._request_handler(request)

    async def _request_handler(self, request: RestRequest):
        try:
            if request.delay:
                await asyncio.sleep(request.delay)

            response = request.send(self.request_timeout)

            self.received_request_responses.append(response)
            self.sent_requests.append(request)

        except (ConnectTimeout, ReadTimeout) as ex:
            error_message = "Timed out trying to send request:\n" + str(request)
            raise WSTimeoutError(error_message) from ex

    def _get_connection_string(self) -> str:
        # wss://example.com?first=123&second=456
        connection_string = self.uri.strip()
        if self.parameters:
            params = "&".join(f"{str(key).strip()}={str(value).strip()}" for key, value in self.parameters.items())
            connection_string += f"?{params}"
        return connection_string

    def _get_receive_error_message(self) -> str:
        error_message = "Timed out waiting for responses:"
        for response in self.expected_responses:
            error_message += "\n" + str(response)

        if self.log_responses_on_error:
            error_message += "\nReceived responses:"
            for json_response in self.received_json:
                error_message += "\n" + str(json_response)

        return error_message

    def is_complete(self) -> bool:
        """
        Checks whether the test has finished running

        Returns:
            (bool): Value to indicate whether the test has finished
        """
        return not self.expected_responses and not self.messages and not self.requests
