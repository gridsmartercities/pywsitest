import unittest
from src.ws_test import WSTest


class WSTestTests(unittest.TestCase):


    def test_create_ws_test_with_uri(self):
        uri = "wss://example.com"
        self.ws_tester = WSTest(uri)

        self.assertEqual(uri, self.ws_tester.uri)

    def test_add_key_value_query_parameter(self):
        key = "example"
        value = 123

        self.ws_tester.with_query_parameter(key, value)

        self.assertEqual(value, self.ws_tester.query_parameters[key])

        