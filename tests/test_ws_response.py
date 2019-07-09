import unittest
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

    def test_with_attribute_value(self):
        ws_response = WSResponse().with_attribute_value("test", 123)

        self.assertEqual(123, ws_response.value_attributes["test"])
        self.assertEqual(1, len(ws_response.value_attributes))

    def test_all_is_match(self):
        ws_response = (WSResponse()
                       .with_attribute_value("type", "new_request")
                       .with_attribute("body"))

        test_data = {
            "type": "new_request",
            "body": {}
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_attribute_value_is_match(self):
        ws_response = (WSResponse()
                       .with_attribute_value("type", "new_request")
                       .with_attribute("body"))

        test_data = {
            "type": "new_request",
            "not_body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_attribute_is_match(self):
        ws_response = (WSResponse()
                       .with_attribute_value("type", "new_request")
                       .with_attribute("body"))

        test_data = {
            "not_type": "new_request",
            "body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_none_is_match(self):
        ws_response = (WSResponse()
                       .with_attribute_value("type", "new_request")
                       .with_attribute("body"))

        test_data = {
            "not_type": "new_request",
            "not_body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))
