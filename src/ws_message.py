import json


class WSMessage:
    """
    A class representing a message to send through the websocket

    Attributes:
        attributes (dict)

    Methods:
        with_attribute(key, value):
            Adds an attribute and returns the WSMessage
    """

    def __init__(self):
        self.attributes = {}

    def __str__(self):
        return json.dumps(self.attributes)

    def with_attribute(self, key, value):
        """
        Adds a key/value pair to the attributes dictionary
        Returns the WSMessage instance

        Parameters:
            key (obj): The key of the attribute
            value (obj): The value of the attribute

        Returns:
            (WSMessage): The WSMessage instance with_attribute was called on
        """
        self.attributes[key] = value
        return self
