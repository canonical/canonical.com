import unittest
from unittest.mock import patch

from canonicalwebteam.discourse import RateLimitedError

from webapp import app as app_module
from webapp.app import app


class TestRateLimitedErrorHandling(unittest.TestCase):
    """
    RateLimitedError from the discourse package must surface as a 503
    with Retry-After, never a 500, and the body format must match what
    the client accepts.
    """

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        patcher = patch.object(
            app_module.engage_pages,
            "get_index",
            side_effect=RateLimitedError(retry_after=77),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_rate_limited_page_returns_styled_503(self):
        response = self.client.get("/case-study")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.headers.get("Retry-After"), "77")
        self.assertTrue(response.content_type.startswith("text/html"))

    def test_rate_limited_json_accept_header_returns_json_503(self):
        response = self.client.get(
            "/case-study", headers={"Accept": "application/json"}
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.headers.get("Retry-After"), "77")
        self.assertTrue(response.content_type.startswith("application/json"))

    def test_retry_after_defaults_to_60_without_hint(self):
        with patch.object(
            app_module.engage_pages,
            "get_index",
            side_effect=RateLimitedError(retry_after=None),
        ):
            response = self.client.get("/case-study")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.headers.get("Retry-After"), "60")


if __name__ == "__main__":
    unittest.main()
