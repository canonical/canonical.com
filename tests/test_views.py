import unittest
from unittest.mock import patch, MagicMock
import flask
import requests
import datetime
from webapp.views import (
    json_asset_query,
    build_events_index,
    build_canonical_days_index,
)


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

    # Events Index Tests
    @patch("webapp.views.flask.render_template")
    def test_events_index_success(self, mock_render_template):
        """Test successful events index retrieval"""
        mock_engage_docs = MagicMock()

        # Mock event data
        events_data = [
            {
                "topic_name": "Ubuntu 24.04 Release",
                "event_location": "San Francisco",
                "event_date": "15/02/2026",
                "path": "/engage/event-1",
            },
            {
                "topic_name": "Cloud Native Conference",
                "event_location": "New York",
                "event_date": "20/03/2026",
                "path": "/engage/event-2",
            },
        ]

        mock_engage_docs.get_index.return_value = (events_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        events_index = build_events_index(mock_engage_docs)

        with self.app.test_request_context():
            events_index()
            mock_render_template.assert_called_once()
            call_kwargs = mock_render_template.call_args[1]
            self.assertIn("metadata", call_kwargs)
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 2)

    @patch("webapp.views.flask.render_template")
    def test_events_index_filters_without_topic_name(
        self, mock_render_template
    ):
        """Test that events without topic_name are filtered out"""
        mock_engage_docs = MagicMock()

        events_data = [
            {
                "topic_name": "Valid Event",
                "event_location": "San Francisco",
                "event_date": "15/02/2026",
            },
            {"event_location": "New York", "event_date": "20/03/2026"},
        ]

        mock_engage_docs.get_index.return_value = (events_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        events_index = build_events_index(mock_engage_docs)

        with self.app.test_request_context():
            events_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 1)
            self.assertEqual(metadata[0]["topic_name"], "Valid Event")

    @patch("webapp.views.flask.render_template")
    @patch("webapp.views.geocode_location")
    def test_events_index_location_search(
        self, mock_geocode, mock_render_template
    ):
        """Test events index with location-based search"""
        mock_engage_docs = MagicMock()

        events_data = [
            {
                "topic_name": "Event 1",
                "event_location": "San Francisco",
                "event_date": "15/02/2026",
            },
            {
                "topic_name": "Event 2",
                "event_location": "New York",
                "event_date": "20/03/2026",
            },
        ]

        mock_engage_docs.get_index.return_value = (events_data, 2, 2, 2)

        # Mock geocode location results
        mock_location = MagicMock()
        mock_location.latitude = 37.7749
        mock_location.longitude = -122.4194
        mock_geocode.return_value = mock_location
        mock_render_template.return_value = "Rendered template"

        events_index = build_events_index(mock_engage_docs)

        with self.app.test_request_context("/?q=San%20Francisco"):
            events_index()
            call_kwargs = mock_render_template.call_args[1]
            self.assertIn("metadata", call_kwargs)

    @patch("webapp.views.flask.render_template")
    @patch("webapp.views.geocode_location")
    def test_events_index_keyword_search(
        self, mock_geocode, mock_render_template
    ):
        """Test events index with keyword-based search"""
        mock_engage_docs = MagicMock()

        events_data = [
            {
                "topic_name": "Ubuntu Release Event",
                "event_location": "San Francisco",
                "event_date": "15/02/2026",
            },
            {
                "topic_name": "Kubernetes Workshop",
                "event_location": "New York",
                "event_date": "20/03/2026",
            },
        ]

        mock_engage_docs.get_index.return_value = (events_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"
        # Return None to trigger keyword search instead of geolocation search
        mock_geocode.return_value = None

        events_index = build_events_index(mock_engage_docs)

        with self.app.test_request_context("/?q=Ubuntu"):
            events_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 1)
            self.assertEqual(metadata[0]["topic_name"], "Ubuntu Release Event")

    @patch("webapp.views.flask.render_template")
    def test_events_index_filters_past_events(self, mock_render_template):
        """Test that past events are filtered out"""
        mock_engage_docs = MagicMock()

        # Create dates: one in past, one in future
        past_date = (
            datetime.datetime.now() - datetime.timedelta(days=10)
        ).strftime("%d/%m/%Y")
        future_date = (
            datetime.datetime.now() + datetime.timedelta(days=10)
        ).strftime("%d/%m/%Y")

        events_data = [
            {
                "topic_name": "Past Event",
                "event_location": "San Francisco",
                "event_date": past_date,
            },
            {
                "topic_name": "Future Event",
                "event_location": "New York",
                "event_date": future_date,
            },
        ]

        mock_engage_docs.get_index.return_value = (events_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        events_index = build_events_index(mock_engage_docs)

        with self.app.test_request_context("/?q=test"):
            events_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 1)
            self.assertEqual(metadata[0]["topic_name"], "Future Event")

    # Canonical Days Tests
    @patch("webapp.views.flask.render_template")
    def test_canonical_days_index_success(self, mock_render_template):
        """Test successful canonical days index retrieval"""
        mock_engage_docs = MagicMock()

        future_date = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")

        roadshow_data = [
            {
                "topic_name": "Canonical Days - London",
                "event_location": "London",
                "event_region": "EMEA",
                "event_date": future_date,
                "path": "/engage/roadshow-london",
            },
            {
                "topic_name": "Canonical Days - Sydney",
                "event_location": "Sydney",
                "event_region": "APAC",
                "event_date": future_date,
                "path": "/engage/roadshow-sydney",
            },
        ]

        mock_engage_docs.get_index.return_value = (roadshow_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        canonical_days_index = build_canonical_days_index(mock_engage_docs)

        with self.app.test_request_context():
            canonical_days_index()
            call_kwargs = mock_render_template.call_args[1]
            self.assertIn("metadata", call_kwargs)
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 2)
            # Verify get_index was called with correct parameters
            mock_engage_docs.get_index.assert_called_once()
            call_args = mock_engage_docs.get_index.call_args
            self.assertEqual(call_args[1]["tag_value"], "roadshow")
            self.assertEqual(call_args[1]["key"], "type")
            self.assertEqual(call_args[1]["value"], "event")

    @patch("webapp.views.flask.render_template")
    def test_canonical_days_filters_incomplete_events(
        self, mock_render_template
    ):
        """Test that events without required metadata are filtered"""
        mock_engage_docs = MagicMock()

        future_date = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")

        roadshow_data = [
            {
                "topic_name": "Complete Event",
                "event_location": "London",
                "event_region": "EMEA",
                "event_date": future_date,
            },
            {
                "topic_name": "Incomplete Event",
                "event_location": "Sydney",
                # Missing event_region
                "event_date": future_date,
            },
            {
                "topic_name": "Another Incomplete",
                "event_location": "Tokyo",
                "event_region": "APAC",
                # Missing event_date
            },
        ]

        mock_engage_docs.get_index.return_value = (roadshow_data, 3, 3, 3)
        mock_render_template.return_value = "Rendered template"

        canonical_days_index = build_canonical_days_index(mock_engage_docs)

        with self.app.test_request_context():
            canonical_days_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 1)
            self.assertEqual(metadata[0]["topic_name"], "Complete Event")

    @patch("webapp.views.flask.render_template")
    def test_canonical_days_filters_past_events(self, mock_render_template):
        """Test that past roadshow events are filtered out"""
        mock_engage_docs = MagicMock()

        past_date = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")
        future_date = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")

        roadshow_data = [
            {
                "topic_name": "Past Roadshow",
                "event_location": "London",
                "event_region": "EMEA",
                "event_date": past_date,
            },
            {
                "topic_name": "Future Roadshow",
                "event_location": "Sydney",
                "event_region": "APAC",
                "event_date": future_date,
            },
        ]

        mock_engage_docs.get_index.return_value = (roadshow_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        canonical_days_index = build_canonical_days_index(mock_engage_docs)

        with self.app.test_request_context():
            canonical_days_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(len(metadata), 1)
            self.assertEqual(metadata[0]["topic_name"], "Future Roadshow")

    @patch("webapp.views.flask.render_template")
    def test_canonical_days_sorts_by_latest_event(self, mock_render_template):
        """Test that roadshow events are sorted by latest date"""
        mock_engage_docs = MagicMock()

        date1 = (
            datetime.datetime.now() + datetime.timedelta(days=10)
        ).strftime("%d/%m/%Y")
        date2 = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")

        roadshow_data = [
            {
                "topic_name": "Earlier Event",
                "event_location": "London",
                "event_region": "EMEA",
                "event_date": date1,
            },
            {
                "topic_name": "Later Event",
                "event_location": "Sydney",
                "event_region": "APAC",
                "event_date": date2,
            },
        ]

        mock_engage_docs.get_index.return_value = (roadshow_data, 2, 2, 2)
        mock_render_template.return_value = "Rendered template"

        canonical_days_index = build_canonical_days_index(mock_engage_docs)

        with self.app.test_request_context():
            canonical_days_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(metadata[0]["topic_name"], "Later Event")
            self.assertEqual(metadata[1]["topic_name"], "Earlier Event")

    @patch("webapp.views.flask.render_template")
    def test_canonical_days_prefixes_engage_paths_with_full_url(
        self, mock_render_template
    ):
        """Test that engage paths are prefixed with full URL"""
        mock_engage_docs = MagicMock()

        future_date = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%d/%m/%Y")

        roadshow_data = [
            {
                "topic_name": "Roadshow",
                "event_location": "London",
                "event_region": "EMEA",
                "event_date": future_date,
                "path": "/engage/roadshow",
            }
        ]

        mock_engage_docs.get_index.return_value = (roadshow_data, 1, 1, 1)
        mock_render_template.return_value = "Rendered template"

        canonical_days_index = build_canonical_days_index(mock_engage_docs)

        with self.app.test_request_context():
            canonical_days_index()
            call_kwargs = mock_render_template.call_args[1]
            metadata = call_kwargs["metadata"]
            self.assertEqual(
                metadata[0]["path"], "https://ubuntu.com/engage/roadshow"
            )


if __name__ == "__main__":
    unittest.main()
