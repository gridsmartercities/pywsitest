import json
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

    def __str__(self):
        return json.dumps(self.attributes)

    def with_attribute(self, attribute, value=None):
        """
        Adds a key/value pair to the attributes dictionary

        Parameters:
            key (obj): The key of the attribute
            value (obj, optional): The value of the attribute

        Returns:
            (WSResponse): The WSResponse instance with_attribute was called on
        """
        self.attributes[attribute] = value
        return self

    def with_trigger(self, message: WSMessage):
        """
        Adds a trigger to the triggers list

        Parameters:
            message (WSMessage): The message object to send to the websocket

        Returns:
            (WSResponse): The WSResponse instance with_trigger was called on
        """
        self.triggers.append(message)
        return self

    def is_match(self, response: dict):
        """
        Checks if this WSResponse instance matches an input response by checking all attributes are present

        Parameters:
            response (dict): The response to check against for a match

        Returns:
            (bool): True if the response matches based on the attributes
        """
        for key in self.attributes:
            if key not in response:
                return False
            # Check attribute values only if value isn't none
            if self.attributes[key] is not None and response[key] != self.attributes[key]:
                return False
        return True
