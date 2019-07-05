import unittest
from src.ws_test import WSTest


class WSTestTests(unittest.TestCase):


    def test_create_ws_test_with_uri(self):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        self.assertEqual(uri, ws_tester.uri)

    def test_add_key_value_query_parameter(self):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        key = "example"
        value = 123

        ws_tester.with_query_parameter(key, value)

        self.assertEqual(value, ws_tester.query_parameters[key])

        