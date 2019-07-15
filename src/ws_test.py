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

    def with_parameter(self, key, value):
        self.query_parameters[key] = value
        return self

    def with_response(self, response: WSResponse):
        self.expected_responses.append(response)
        return self

    async def run(self):
        websocket = await websockets.connect(self._get_connection_string(), ssl=ssl.SSLContext())
        await self.receive(websocket)
        await websocket.close()

    async def receive(self, websocket):
        while self.expected_responses:
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            self.receive_handler(response)

    def receive_handler(self, response):
        parsed_response = json.loads(response)
        self.received_responses.append(response)
        for expected_response in self.expected_responses:
            if expected_response.is_match(parsed_response):
                self.actual_responses.append(expected_response)
                self.expected_responses.remove(expected_response)
                break

    # async def send(self, websocket):
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
