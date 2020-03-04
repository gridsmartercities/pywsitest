import json

from .utils import get_resolved_values, PATH_REGEX


class WSMessage:
    """
    A class representing a message to send through the websocket

    Attributes:
        attributes (dict)

    Methods:
        with_attribute(key, value):
            Adds an attribute and returns the WSMessage
        with_delay(delay):
            Adds a delay to message being sent
        resolve(response):
            Resolves any attributes that get their value from a parent response

    Usage:
        message = (
            WSMessage()
            .with_attribute("test", "example")
        )
    """

    def __init__(self):
        self.attributes = {}
        self.delay = 0.0

    def __str__(self) -> str:
        # Output the attributes dictionary as json
        return json.dumps(self.attributes)

    def with_attribute(self, key: str, value: object) -> "WSMessage":
        """
        Adds a key/value pair to the attributes dictionary

        Parameters:
            key (str): The key of the attribute
            value (obj): The value of the attribute

        Returns:
            (WSMessage): The WSMessage instance with_attribute was called on
        """
        self.attributes[key] = value
        return self

    def with_delay(self, delay: float) -> "WSMessage":
        """
        Adds a delay (in seconds) to the message sending

        Parameters:
            delay (float): The time to wait before sending the message in seconds

        Returns:
            (WSMessage): The WSMessage instance with_delay was called on
        """
        self.delay = delay
        return self

    def resolve(self, response: dict) -> "WSMessage":
        """
        Resolves attributes using ${path/to/property} notation with response as the source

        Parameters:
            response (dict): The response object to resolve attributes from

        Returns:
            (WSMessage): The WSMessage instance resolve was called on
        """
        for key in self.attributes:
            value = self.attributes[key]
            match = PATH_REGEX.match(str(value))
            if match:
                resolved_values = get_resolved_values(response, match.group(1))
                self.attributes[key] = resolved_values[0] if resolved_values else value
        return self
