import unittest
from unittest.mock import patch, MagicMock
from src.ws_response import WSResponse

class WSResponseTests(unittest.TestCase):

    def test_create_ws_response(self):
        ws_response = WSResponse()

        self.assertListEqual([], ws_response.attributes)
        self.assertDictEqual({}, ws_response.value_attributes)

    def test_with_attribute(self):
        ws_response = WSResponse().with_attribute("test")

        self.assertIn("test", ws_response.attributes)
        self.assertEqual(1, len(ws_response.attributes))