import json

from .utils import get_resolved_values
from .ws_message import WSMessage


class WSResponse:
    """
    A class representing an expected message to be received through the websocket

    Attributes:
        attributes (dict)
        triggers (list)

    Methods:
        with_attribute(key, value=None):
            Adds an attribute and returns the WSResponse
        with_trigger(message: WSResponse):
            Adds a trigger and returns the WSResponse
        is_match(response: dict):
            Checks if this WSResponse instance matches an input response and returns the result as a bool

    Usage:
        response = (
            WSResponse()
            .with_attribute("type", "example")
            .with_attribute("body")
            .with_trigger(
                WSMessage()
            )
        )
    """

    def __init__(self):
        self.attributes = {}
        self.triggers = []

    def __str__(self) -> str:
        return json.dumps(self.attributes)

    def with_attribute(self, attribute: str, value: object = None) -> "WSResponse":
        """
        Adds a key/value pair to the attributes dictionary

        Parameters:
            attribute (str): The key of the attribute
            value (obj, optional): The value of the attribute

        Returns:
            (WSResponse): The WSResponse instance with_attribute was called on
        """
        self.attributes[attribute] = value
        return self

    def with_trigger(self, message: WSMessage) -> "WSResponse":
        """
        Adds a trigger to the triggers list

        Parameters:
            message (WSMessage): The message object to send to the websocket

        Returns:
            (WSResponse): The WSResponse instance with_trigger was called on
        """
        self.triggers.append(message)
        return self

    def is_match(self, response: dict) -> bool:
        """
        Checks if this WSResponse instance matches an input response by checking all attributes are present

        Parameters:
            response (dict): The response to check against for a match

        Returns:
            (bool): True if the response matches based on the attributes
        """
        for key in self.attributes:
            resolved_values = get_resolved_values(response, key)

            if not resolved_values:
                return False

            if self.attributes[key] is None:
                continue

            if any(self.attributes[key] == value for value in resolved_values):
                continue

            return False

        return True
