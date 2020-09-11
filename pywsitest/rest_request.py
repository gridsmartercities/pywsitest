import requests


class RestRequest:

    def __init__(self, uri: str, method: str):
        self.uri = uri
        self.method = method.casefold()
        self.headers = {}
        self.body = {}
        self.delay = 0.0

    def with_header(self, key: str, value: str) -> "RestRequest":
        self.headers[key] = value
        return self

    def with_body(self, body: dict) -> "RestRequest":
        self.body = body
        return self

    def with_delay(self, delay: float) -> "RestRequest":
        self.delay = delay
        return self

    def send(self, timeout: float):
        kwargs = {"timeout": timeout}
        if self.headers:
            kwargs["headers"] = self.headers
        if self.body:
            kwargs["json"] = self.body

        return requests.request(self.method, self.uri, **kwargs)
