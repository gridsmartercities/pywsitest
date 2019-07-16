import unittest
from src.ws_message import WSMessage


class WSMessageTests(unittest.TestCase):

    def test_create_ws_message(self):
        ws_message = WSMessage()

        self.assertDictEqual({}, ws_message.attributes)

    def test_with_attribute(self):
        ws_message = WSMessage().with_attribute("test", 123)

        self.assertIn("test", ws_message.attributes)
        self.assertEqual(1, len(ws_message.attributes))

    def test_stringify_with_attribute(self):
        ws_message = WSMessage().with_attribute("test", 123)

        expected_value = "{\"test\": 123}"
        self.assertEqual(expected_value, str(ws_message))
