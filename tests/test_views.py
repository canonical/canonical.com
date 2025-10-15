import unittest
from unittest.mock import patch, MagicMock
import flask
import requests
from webapp.views import json_asset_query


class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("webapp.views.requests.get")
    def test_json_asset_query_success(self, mock_get):
        """Test successful JSON asset retrieval"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        with self.app.test_request_context():
            result = json_asset_query("test.json")
            self.assertEqual(result.get_json(), {"key": "value"})
            mock_get.assert_called_once_with(
                url="https://assets.ubuntu.com/v1/test.json"
            )

    @patch("webapp.views.requests.get")
    @patch("webapp.views.flask.current_app")
    def test_json_asset_query_http_error(self, mock_app, mock_get):
        """Test HTTP error handling"""
        # Mock HTTPError
        mock_get.side_effect = requests.HTTPError("404 Not Found")
        mock_sentry = MagicMock()
        mock_app.extensions = {"sentry": mock_sentry}

        with self.app.test_request_context():
            result = json_asset_query("nonexistent.json")
            self.assertEqual(result[1], 404)
            self.assertEqual(
                result[0].get_json(), {"error": "Asset not found"}
            )
            mock_sentry.captureException.assert_called_once()
