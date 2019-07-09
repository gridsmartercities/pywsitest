class WSResponse:

    def __init__(self):
        self.attributes = []
        self.value_attributes = {}

    def with_attribute(self, attribute):
        self.attributes.append(attribute)
        return self

    def with_attribute_value(self, attribute, value):
        self.value_attributes[attribute] = value
        return self

    def is_match(self, response):
        for key in self.attributes:
            if key not in response:
                return False
        for key in self.value_attributes:
            if response.get(key) != self.value_attributes[key]:
                return False
        return True
