import unittest
from webapp.openapi_parser import parse_openapi, read_yaml_from_file


class TestOpenApiParser(unittest.TestCase):
    def test_openapi_parser(self):
        EXPECTED_OUTPUT = {
            "Logged-in user": [
                {
                    "/account/op-create_authorisation_token": {
                        "post": {
                            "description": (
                                "Create an authorisation OAuth token and "
                                "OAuth consumer."
                            ),
                            "operationId": (
                                "AccountHandler_create_authorisation_token"
                            ),
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "additionalProperties": True,
                                                "type": "object",
                                            }
                                        }
                                    },
                                    "description": (
                                        "A JSON object containing: "
                                        "``token_key``, ``token_secret``, "
                                        "``consumer_key``, and ``name``."
                                    ),
                                }
                            },
                            "summary": "Create an authorisation token",
                            "tags": ["Logged-in user"],
                        }
                    }
                }
            ]
        }

        definition = read_yaml_from_file("tests/openapi_example.yaml")
        output = parse_openapi(definition)
        self.assertEqual(output, EXPECTED_OUTPUT)


if __name__ == "__main__":
    unittest.main()
