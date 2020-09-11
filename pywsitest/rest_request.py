import requests


class RestRequest:
    """
    A class representing a rest request

    Attributes:
        uri (str)
        method (str)
        headers (dict)
        body (dict)
        delay (float)

    Methods:
        with_header(key (str), value (str)):
            Adds a header and returns RestRequest
        with_body(body (dict)):
            Adds a body and returns RestRequest
        with_delay(delay (float)):
            Adds a delay and returns RestRequest
        send(timeout (float)):
            Composes and sends rest request, returning request response

    Usage:
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_header("Authorization", "jwt_token")
            .with_body({"abc": 123})
            .with_delay(1.0)
        )

        rest_request.send(10.0)
    """

    def __init__(self, uri: str, method: str):
        """
            Parameters:
                uri (str): The uri of the rest api
                method (str): The type/method of the request (get/post/patch/etc...)
        """
        self.uri = uri
        self.method = method.casefold()
        self.headers = {}
        self.body = {}
        self.delay = 0.0

    def with_header(self, key: str, value: str) -> "RestRequest":
        """
        Adds a key/value pair to the header dictionary
        Headers are standard rest api request headers

        Parameters:
            key (str): The key of the header
            value (str): The value of the header

        Returns:
            (RestRequest): The RestRequest instance with_header was called on
        """
        self.headers[key] = value
        return self

    def with_body(self, body: dict) -> "RestRequest":
        """
        Adds a dictionary representing request body

        Parameters:
            body (dict): The dictionary representing request body

        Returns:
            (RestRequest): The RestRequest instance with_body was called on
        """
        self.body = body
        return self

    def with_delay(self, delay: float) -> "RestRequest":
        """
        Adds a delay to the rest request

        Parameters:
            delay (float): The number of seconds to be delayed

        Returns:
            (RestRequest): The RestRequest instance with_delay was called on
        """
        self.delay = delay
        return self

    def send(self, timeout: float):
        """
        Composes and sends the rest request
        Receives any responses from the api and returns that response

        Returns:
            (Response): An instance of a response object with the response of the rest api
        """
        kwargs = {"timeout": timeout}
        if self.headers:
            kwargs["headers"] = self.headers
        if self.body:
            kwargs["json"] = self.body

        return requests.request(self.method, self.uri, **kwargs)
