import json
import re


class WSMessage:
    """
    A class representing a message to send through the websocket

    Attributes:
        attributes (dict)

    Methods:
        with_attribute(key, value):
            Adds an attribute and returns the WSMessage
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

    def __str__(self):
        # Output the attributes dictionary as json
        return json.dumps(self.attributes)

    def with_attribute(self, key, value):
        """
        Adds a key/value pair to the attributes dictionary

        Parameters:
            key (obj): The key of the attribute
            value (obj): The value of the attribute

        Returns:
            (WSMessage): The WSMessage instance with_attribute was called on
        """
        self.attributes[key] = value
        return self

    def resolve(self, response):
        """
        Resolves attributes using ${path/to/property} notation with response as the source

        Parameters:
            response (dict): The response object to resolve attributes from
        
        Returns:
            (WSMessage): The WSMessage instance resolve was called on
        """
        regex = re.compile("^\$\{(.*)\}$")  # noqa: pylint - anomalous-backslash-in-string
        for key in self.attributes:
            value = self.attributes[key]
            match = regex.match(str(value))
            if match:
                resolved = self._get_resolved_value(response, match.group(1))
                self.attributes[key] = resolved if resolved else value
        return self

    def _get_resolved_value(self, response, path):  # noqa: pylint - no-self-use
        resolved = response
        for part in path.split("/"):
            if part in resolved:
                resolved = resolved[part]
            else:
                return None
        return resolved
