import unittest
from src.ws_test import WSTest


class WSTestTests(unittest.TestCase):

    def test_create_ws_test_with_uri(self):
        uri = "wss://example.com"
        ws_tester = WSTest(uri)

        self.assertEqual(uri, ws_tester.uri)