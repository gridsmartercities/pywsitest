import unittest

from pywsitest import WSMessage


class WSMessageTests(unittest.TestCase):

    def test_create_ws_message(self):
        ws_message = WSMessage()

        self.assertDictEqual({}, ws_message.attributes)

    def test_with_attribute(self):
        ws_message = WSMessage().with_attribute("test", 123)

        self.assertIn("test", ws_message.attributes)
        self.assertEqual(1, len(ws_message.attributes))

    def test_with_delay(self):
        ws_message = (
            WSMessage()
            .with_attribute("test", 123)
            .with_delay(0.1)
        )

        self.assertEqual(0.1, ws_message.delay)

    def test_stringify_with_attribute(self):
        ws_message = WSMessage().with_attribute("test", 123)

        expected_value = "{\"test\": 123}"
        self.assertEqual(expected_value, str(ws_message))

    def test_resolve_attribute(self):
        ws_message = (
            WSMessage()
            .with_attribute("test", 123)
            .with_attribute("example", "${body/example}")
        )

        response = {
            "type": "message",
            "body": {
                "example": 456
            }
        }

        expected_value = "{\"test\": 123, \"example\": 456}"

        ws_message = ws_message.resolve(response)

        self.assertEqual(expected_value, str(ws_message))
