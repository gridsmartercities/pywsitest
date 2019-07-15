import asyncio
import json
import ssl
import websockets
from src.ws_response import WSResponse


class WSTest:

    def __init__(self, uri):
        self.uri = uri
        self.query_parameters = {}
        self.expected_responses = []
        self.actual_responses = []
        self.received_responses = []
        self.response_timeout = 10.0

    def with_parameter(self, key, value):
        self.query_parameters[key] = value
        return self

    def with_response(self, response: WSResponse):
        self.expected_responses.append(response)
        return self

    def with_response_timeout(self, timeout):
        self.response_timeout = timeout
        return self

    async def run(self):
        websocket = await websockets.connect(self._get_connection_string(), ssl=ssl.SSLContext())
        try:
            await self._receive(websocket)
        finally:
            await websocket.close()

    async def _receive(self, websocket):
        while self.expected_responses:
            response = await asyncio.wait_for(websocket.recv(), timeout=self.response_timeout)
            self._receive_handler(response)

    def _receive_handler(self, response):
        self.received_responses.append(response)
        parsed_response = json.loads(response)

        for expected_response in self.expected_responses:
            if expected_response.is_match(parsed_response):
                self.actual_responses.append(expected_response)
                self.expected_responses.remove(expected_response)
                break

    # async def _send(self, websocket):
    #     pass

    def _get_connection_string(self):
        connection_string = self.uri
        if self.query_parameters:
            connection_string += "?"
        for key in self.query_parameters:
            connection_string += str(key) + "=" + str(self.query_parameters[key]) + "&"
        return connection_string.strip("&")

    def is_complete(self):
        return not self.expected_responses
