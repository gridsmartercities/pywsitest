import unittest

from pywsitest import WSResponse, WSMessage


class WSResponseTests(unittest.TestCase):  # noqa: pylint - too-many-public-methods

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

    def test_resolved_recursive_attribute_match(self):
        ws_response = WSResponse().with_attribute("body/first/second/third", "value")

        test_data = {
            "type": "new_request",
            "body": {
                "first": {
                    "second": {
                        "third": "value",
                        "fourth": "not_value"
                    }
                }
            }
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_resolved_attribute_by_list_index(self):
        ws_response = WSResponse().with_attribute("body[0]colour", "red")

        test_data = {
            "body": [
                {"colour": "red"},
                {"colour": "green"},
                {"colour": "blue"}
            ]
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_resolved_attribute_by_list_without_index(self):
        ws_response = WSResponse().with_attribute("body[]colour", "green")

        test_data = {
            "body": [
                {"colour": "red"},
                {"colour": "green"},
                {"colour": "blue"}
            ]
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_resolved_attribute_by_list_index_no_match(self):
        ws_response = WSResponse().with_attribute("body[1]colour", "yellow")

        test_data = {
            "body": [
                {"colour": "red"},
                {"colour": "green"},
                {"colour": "blue"}
            ]
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_resolved_attribute_by_list_index_not_enough_elements(self):
        ws_response = WSResponse().with_attribute("body[0]colour", "red")

        test_data = {
            "body": []
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_resolved_attribute_by_list_without_index_no_match(self):
        ws_response = WSResponse().with_attribute("body[]colour", "yellow")

        test_data = {
            "body": [
                {"colour": "red"},
                {"colour": "green"},
                {"colour": "blue"}
            ]
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_resolved_attribute_by_just_list_index(self):
        ws_response = WSResponse().with_attribute("body[0]", "red")

        test_data = {
            "body": [
                "red",
                "green",
                "blue"
            ]
        }

        self.assertTrue(ws_response.is_match(test_data))

    def test_resolve_by_index_when_dict_fails(self):
        ws_response = WSResponse().with_attribute("body[0]colour", "red")

        test_data = {
            "body": {
                "colour": "red"
            }
        }

        self.assertFalse(ws_response.is_match(test_data))

    def test_resolve_by_key_when_list_fails(self):
        ws_response = WSResponse().with_attribute("body/colour", "red")

        test_data = {
            "body": [
                "red",
                "green",
                "blue"
            ]
        }

        self.assertFalse(ws_response.is_match(test_data))
