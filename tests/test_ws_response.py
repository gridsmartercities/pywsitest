import unittest
from pywsitest import WSResponse, WSMessage


class WSResponseTests(unittest.TestCase):

    def test_create_ws_response(self):
        ws_response = WSResponse()

        self.assertDictEqual({}, ws_response.attributes)

    def test_with_attribute(self):
        ws_response = WSResponse().with_attribute("test")

        self.assertIn("test", ws_response.attributes)
        self.assertEqual(1, len(ws_response.attributes))

    def test_with_attribute_with_value(self):
        ws_response = WSResponse().with_attribute("test", 123)

        self.assertEqual(123, ws_response.attributes["test"])
        self.assertEqual(1, len(ws_response.attributes))

    def test_all_attributes_is_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body")
        )

        test_data = {
            "type": "new_request",
            "body": {}
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_attribute_is_not_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body")
        )

        test_data = {
            "type": "new_request",
            "not_body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_attribute_value_is_not_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body")
        )

        test_data = {
            "type": "not_new_request",
            "body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_no_attributes_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body")
        )

        test_data = {
            "not_type": "new_request",
            "not_body": {}
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_with_trigger(self):
        message = WSMessage().with_attribute("test", 123)
        ws_response = WSResponse().with_trigger(message)

        self.assertEqual(1, len(ws_response.triggers))
        self.assertEqual(message, ws_response.triggers[0])

    def test_stringify(self):
        response = WSResponse().with_attribute("test", 123)
        self.assertEqual("{\"test\": 123}", str(response))

    def test_resolved_attribute_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body/attribute", "value")
        )

        test_data = {
            "type": "new_request",
            "body": {
                "attribute": "value"
            }
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_no_resolved_attribute_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body/attribute", "value")
        )

        test_data = {
            "type": "new_request",
            "body": {
                "not_attribute": "not_value"
            }
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_resolved_attribute_no_match(self):
        ws_response = (
            WSResponse()
            .with_attribute("type", "new_request")
            .with_attribute("body/attribute", "value")
        )

        test_data = {
            "type": "new_request",
            "body": {
                "attribute": "not_value"
            }
        }

        self.assertFalse(ws_response.is_match(test_data))
