import json


class WSMessage:
    def __init__(self):
        self.attributes = {}

    def with_attribute(self, key):
        self.attributes[key] = None
        return self

    def __str__(self):
        return json.dumps(self.attributes)
