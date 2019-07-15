class WSResponse:

    def __init__(self):
        self.attributes = {}

    def with_attribute(self, attribute, value=None):
        self.attributes[attribute] = value
        return self

    def is_match(self, response):
        for key in self.attributes:
            if key not in response:
                return False
            if self.attributes[key] is not None and response[key] != self.attributes[key]:
                return False
        return True
