import unittest
from unittest.mock import patch, MagicMock

from pywsitest import RestRequest


class RestRequestTests(unittest.TestCase):

    def test_create_rest_request_with_uri_and_method(self):
        rest_request = RestRequest("https://example.com", "POST")
        self.assertEqual(rest_request.uri, "https://example.com")
        self.assertEqual(rest_request.method, "post")

    def test_create_rest_request_with_authorization_header(self):
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_header("Authorization", "jwt_token")
        )

        self.assertIn("Authorization", rest_request.headers)
        self.assertEqual(rest_request.headers.get("Authorization"), "jwt_token")

    def test_create_rest_request_with_multiple_headers(self):
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_header("Authorization", "jwt_token")
            .with_header("Format", "json")
        )

        self.assertEqual(rest_request.headers.get("Authorization"), "jwt_token")
        self.assertEqual(rest_request.headers.get("Format"), "json")

    def test_create_rest_request_with_body(self):
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_body({"abc": 123})
        )

        self.assertEqual(rest_request.body, {"abc": 123})

    def test_create_rest_request_with_delay(self):
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_delay(10)
        )

        self.assertEqual(rest_request.delay, 10)

    def test_rest_request_run_success(self):
        rest_request = (
            RestRequest("https://example.com", "POST")
            .with_header("Authorization", "jwt_token")
            .with_body({"abc": 123})
        )

        def mock_handler(*args, **kwargs):  # pylint:disable=unused-argument
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = kwargs.get("json")
            return mock_response

        with patch("requests.request") as mock_request:
            mock_request.side_effect = mock_handler
            response = rest_request.send(10)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"abc": 123})
