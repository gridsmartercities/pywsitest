import json


class WSMessage:

    def __init__(self):
        self.attributes = {}

    def with_attribute(self, key, value):
        self.attributes[key] = value
        return self

    def __str__(self):
        return json.dumps(self.attributes)
