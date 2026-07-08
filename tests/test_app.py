import unittest
from webapp.app import app, is_remote


class TestIsRemote(unittest.TestCase):
    def test_is_remote(self):
        self.assertTrue(is_remote({"location": None}))
        self.assertTrue(is_remote({"location": {"name": None}}))
        self.assertTrue(is_remote({"location": {"name": "Home Based - EMEA"}}))
        self.assertFalse(is_remote({"location": {"name": "Paris, France"}}))


class TestCacheControlHeaders(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_html_page_defaults_to_one_hour_max_age(self):
        """
        Pages that don't set their own Cache-Control should get
        the app-wide 1 hour default, not flask-base's 60 seconds
        """
        response = self.client.get("/legal")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cache_control.max_age, 3600)

    def test_explicit_max_age_is_preserved(self):
        """
        Views that set their own Cache-Control max-age should not
        be overridden by the 1 hour default
        """
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cache_control.public)
        self.assertEqual(response.cache_control.max_age, 43200)

    def test_status_endpoints_are_not_cached(self):
        response = self.client.get("/_status/check")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cache_control.no_store)
        self.assertIsNone(response.cache_control.max_age)

    def test_html_responses_vary_by_cookie(self):
        """
        HTML bodies are rewritten based on the "utms" cookie
        (append_utms_cookie_to_ubuntu_links), so shared caches must
        key HTML responses on the Cookie header
        """
        response = self.client.get("/legal")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cookie", response.vary)

    def test_non_html_responses_do_not_vary_by_cookie(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Cookie", response.vary)
