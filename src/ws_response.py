class WSResponse:

    def __init__(self):
        self.attributes = []
        self.value_attributes = {}

    def with_attribute(self, attribute):
        self.attributes.append(attribute)
        return self
        