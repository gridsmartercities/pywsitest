import asyncio
import websockets
import ssl

class WSTest:

    def __init__(self, uri):
        self.uri = uri
        self.query_parameters = {}

    def with_query_parameter(self, key, value):
        self.query_parameters[key] = value
        return self

    async def run(self):
        websocket = await websockets.connect(self._get_connection_string(), ssl=ssl.SSLContext())
        # perform actions here
        await websocket.close()

    def _get_connection_string(self):
        connection_string = self.uri
        if self.query_parameters:
            connection_string += "?"
        for key in self.query_parameters:
            connection_string += str(key) + "=" + str(self.query_parameters[key]) + "&"
        return connection_string.strip("&") 