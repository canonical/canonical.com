import unittest
from unittest.mock import patch
import os
import importlib
from werkzeug.exceptions import (
    NotFound,
    Forbidden,
    InternalServerError,
    Unauthorized,
    BadRequest,
    TooManyRequests,
)
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    RetryError,
    HTTPError as RequestsHTTPError,
)
from urllib3.exceptions import MaxRetryError
import webapp.app
from webapp.app import sentry_before_send


class TestSentryFiltering(unittest.TestCase):
    """
    Test Sentry error filtering logic.
    """

    def test_filter_404(self):
        """
        Test that 404 (Not Found) errors are filtered out.
        """
        hint = {"exc_info": (None, NotFound(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "404 errors should be filtered")

    def test_filter_403(self):
        """
        Test that 403 (Forbidden) errors are filtered out.
        """
        hint = {"exc_info": (None, Forbidden(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "403 errors should be filtered")

    def test_allow_500(self):
        """
        Test that 500 (Internal Server Error) errors are NOT filtered.
        """
        hint = {"exc_info": (None, InternalServerError(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertEqual(result, event, "500 errors should not be filtered")

    def test_filter_401(self):
        """
        Test that 401 (Unauthorized) errors are filtered out.
        """
        hint = {"exc_info": (None, Unauthorized(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "401 errors should be filtered")

    def test_filter_400(self):
        """
        Test that 400 (Bad Request) errors are filtered out.
        """
        hint = {"exc_info": (None, BadRequest(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "400 errors should be filtered")

    def test_filter_429(self):
        """
        Test that 429 (Too Many Requests) errors are filtered out.
        """
        hint = {"exc_info": (None, TooManyRequests(), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "429 errors should be filtered")

    def test_allow_other_exceptions(self):
        """
        Test that generic exceptions are NOT filtered.
        """
        hint = {"exc_info": (None, Exception("Generic error"), None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertEqual(
            result, event, "Generic exceptions should not be filtered"
        )

    def test_no_exc_info(self):
        """
        Test that events without exception info are passed through.
        """
        hint = {}
        event = {"message": "Some message"}
        result = sentry_before_send(event, hint)
        self.assertEqual(
            result, event, "Events without exc_info should not be filtered"
        )

    def test_drop_blog_api_retry_error_when_sampled_out(self):
        """
        Test that blog API retry errors are dropped 95% of the time
        (when random.random() > 0.05).
        """
        exc = MaxRetryError(None, "/wp-json/wp/v2/posts")
        hint = {"exc_info": (None, exc, None)}
        event = {"level": "error"}
        with patch("webapp.app.random.random", return_value=0.5):
            result = sentry_before_send(event, hint)
        self.assertIsNone(
            result, "Blog API retry errors should be dropped 95% of the time"
        )

    def test_allow_blog_api_retry_error_within_sample(self):
        """
        Test that blog API retry errors pass through 5% of the time
        (when random.random() <= 0.05).
        """
        exc = RetryError("/wp-json/wp/v2/posts connection failed")
        hint = {"exc_info": (None, exc, None)}
        event = {"level": "error"}
        with patch("webapp.app.random.random", return_value=0.03):
            result = sentry_before_send(event, hint)
        self.assertEqual(
            result,
            event,
            "Blog API retry errors within sample should pass through",
        )

    def test_filter_requests_http_error_401(self):
        """
        Test that requests.HTTPError with a 4xx response is filtered out.
        """
        response = unittest.mock.MagicMock()
        response.status_code = 401
        exc = RequestsHTTPError("401 Client Error")
        exc.response = response
        hint = {"exc_info": (None, exc, None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertIsNone(result, "requests HTTPError 4xx should be filtered")

    def test_allow_requests_http_error_500(self):
        """
        Test that requests.HTTPError with a 5xx response is NOT filtered.
        """
        response = unittest.mock.MagicMock()
        response.status_code = 500
        exc = RequestsHTTPError("500 Server Error")
        exc.response = response
        hint = {"exc_info": (None, exc, None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertEqual(
            result, event, "requests HTTPError 5xx should not be filtered"
        )

    def test_allow_non_blog_connection_error(self):
        """
        Test that connection errors unrelated to the blog API
        always pass through.
        """
        exc = RequestsConnectionError("upstream connection failed")
        hint = {"exc_info": (None, exc, None)}
        event = {"level": "error"}
        result = sentry_before_send(event, hint)
        self.assertEqual(
            result, event, "Non-blog connection errors should not be filtered"
        )

    def test_sentry_init_configuration(self):
        """
        Test that sentry_sdk.init is called
        with the correct before_send function.
        """
        with patch("webapp.app.sentry_sdk.init") as mock_init:
            # Set env vars to ensure init is called.
            with patch.dict(
                os.environ,
                {
                    "SENTRY_DSN": "https://key@sentry.io/123",
                    "SECRET_KEY": "test",
                },
            ):
                # Reload webapp.app to trigger the init call
                importlib.reload(webapp.app)

                mock_init.assert_called()
                # Check if before_send was passed in any of the calls
                # (if called multiple times, though it should be once)
                # But module reload might behave weirdly.

                # Check the last call arguments
                call_args = mock_init.call_args[1]
                self.assertIn("before_send", call_args)
                self.assertEqual(
                    call_args["before_send"], webapp.app.sentry_before_send
                )


if __name__ == "__main__":
    unittest.main()
