class WSTest:

    def __init__(self, uri):
        self.uri = uri
        self.query_parameters = {}

    def with_query_parameter(self, key, value):
        self.query_parameters[key] = value
        return self