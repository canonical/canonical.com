import logging
import os
import responses
import unittest
from unittest.mock import patch

from vcr_unittest import VCRTestCase
from webapp.app import app, get_latest_versions
from webapp.handlers import get_canonical_url

logging.getLogger("talisker.context").disabled = True


class TestRoutes(VCRTestCase):
    def _get_vcr_kwargs(self):
        """
        This removes the authorization header
        from VCR so we don't record auth parameters
        """
        return {
            "filter_headers": ["Authorization"],
            # Our cassettes include gzip-compressed response bodies.
            # Enable transparent decoding during playback so callers can
            # safely call `response.json()`.
            "decode_compressed_response": True,
        }

    def setUp(self):
        """
        Set up Flask app for testing
        """

        app.testing = True
        self.client = app.test_client()
        return super(TestRoutes, self).setUp()

    def test_homepage(self):
        """
        When given the index URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/").status_code, 200)

    def test_careers_overview(self):
        """
        When given the /careers index URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/careers").status_code, 200)

    def test_department_page(self):
        """
        When given the index URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/careers/people").status_code, 200)
        self.assertEqual(
            self.client.get("/careers/support-engineering").status_code, 200
        )
        self.assertEqual(
            self.client.get("/careers/marketing").status_code, 200
        )
        self.assertEqual(
            self.client.get("/careers/web-and-design").status_code, 200
        )
        self.assertEqual(
            self.client.get("/careers/administration").status_code, 200
        )

    def test_company_culture_pages(self):
        """
        When given the index URL,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get(
                "/careers/company-culture/remote-work"
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                "/careers/company-culture/sustainability"
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                "/careers/company-culture/progression"
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get("/careers/company-culture/diversity").status_code,
            200,
        )
        self.assertEqual(
            self.client.get("/careers/company-culture").status_code, 200
        )
        self.assertEqual(
            self.client.get("/careers/roles.json").status_code, 200
        )

    def test_invalid_careers_department(self):
        """
        When given the URL of an invalid careers department,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/careers/foo").status_code, 404)

    def test_partners_pages(self):
        """
        When given the URL of a valid parters page,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/partners").status_code, 200)
        self.assertEqual(self.client.get("/partners/desktop").status_code, 200)
        self.assertEqual(
            self.client.get("/partners/channel-and-reseller").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/iot-device").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/ihv-and-oem").status_code, 200
        )
        self.assertEqual(self.client.get("/partners/gsi").status_code, 200)
        self.assertEqual(
            self.client.get("/partners/public-cloud").status_code, 200
        )
        self.assertEqual(self.client.get("/partners/silicon").status_code, 200)
        self.assertEqual(
            self.client.get("/partners/silicon/intel").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/become-a-partner").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/find-a-partner").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/executive-summit").status_code, 200
        )
        self.assertEqual(
            self.client.get("/partners/broadcom").status_code, 200
        )

    def test_invalid_partners_page(self):
        """
        When given the URL of an invalid partners department,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/partners/foo").status_code, 404)

    def test_not_found(self):
        """
        When given a non-existent URL,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/not-found-url").status_code, 404)

    def test_staging_no_robots_header(self):
        """Test that staging does not return a X-Robots-Tag header"""
        os.environ["FLASK_ENV"] = "staging"
        response = self.client.get("/robots.txt")
        self.assertTrue(response.headers["X-Robots-Tag"] == "none")

    def test_production_robots_header(self):
        """Test only production returns X-Robots-Tag header"""
        os.environ["FLASK_ENV"] = "production"
        response = self.client.get("/robots.txt")
        self.assertTrue(response.headers.get("X-Robots-Tag") != "none")

    def test_canonical_drops_query_string(self):
        """Arbitrary query strings must not create self-canonical URLs"""
        for url in (
            "/?q=ocatoto",
            "/?ocatoto",
            "/?s=ocatoto",
            "/?utm_source=x",
        ):
            html = self.client.get(url).get_data(as_text=True)
            self.assertIn(
                '<link rel="canonical" href="http://localhost/" />', html, url
            )

    def test_canonical_keeps_allowlisted_params(self):
        """Parameters that change listing content stay in the canonical"""
        cases = {
            "/blog?page=2&utm_source=x": "http://localhost/blog?page=2",
            "/blog/archives?year=2026&month=3&q=x": (
                "http://localhost/blog/archives?month=3&year=2026"
            ),
            "/case-study?tag=OpenStack&_ga=1": (
                "http://localhost/case-study?tag=OpenStack"
            ),
            "/?page=2&tag=x": "http://localhost/",
        }
        for url, expected in cases.items():
            with app.test_request_context(url):
                self.assertEqual(get_canonical_url(), expected, url)

    def test_homepage_website_jsonld(self):
        """The homepage links a WebSite to the Organization by @id"""
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('"@type": "WebSite"', html)
        self.assertIn('"@id": "https://canonical.com/#organization"', html)

    @patch.dict(os.environ, {"SEARCH_API_KEY": "test-key"})
    def test_search_is_noindex(self):
        """/search is served with noindex and not blocked in robots.txt"""
        os.environ["FLASK_ENV"] = "production"
        response = self.client.get("/search")
        self.assertEqual(response.headers.get("X-Robots-Tag"), "noindex")
        robots = self.client.get("/robots.txt").get_data(as_text=True)
        self.assertNotIn("Disallow: /search\n", robots)

    @patch("webapp.app.flask.render_template", return_value="latest-news")
    @patch("webapp.app.latest_news_blog_views.get_index", return_value={})
    def test_blog_latest_news_defaults_to_page_one(
        self, mock_get_index, mock_render_template
    ):
        response = self.client.get("/blog/latest-news")

        self.assertEqual(response.status_code, 200)
        mock_get_index.assert_called_once_with(page=1)
        mock_render_template.assert_called_once_with("blog/latest-news.html")

    @patch("webapp.app.flask.render_template", return_value="latest-news")
    @patch("webapp.app.latest_news_blog_views.get_index", return_value={})
    def test_blog_latest_news_uses_page_query_param(
        self, mock_get_index, mock_render_template
    ):
        response = self.client.get("/blog/latest-news?page=3")

        self.assertEqual(response.status_code, 200)
        mock_get_index.assert_called_once_with(page=3)
        mock_render_template.assert_called_once_with("blog/latest-news.html")

    def test_ubuntu_pro_description(self):
        """
        When given the /legal/ubuntu-pro-description URL,
        we should return a 200 status code
        """
        self.assertEqual(
            self.client.get("/legal/ubuntu-pro-description").status_code, 200
        )

    def test_ubuntu_pro_description_print(self):
        """
        When given the /legal/ubuntu-pro-description/print URL,
        we should return a 200 status code
        """
        self.assertEqual(
            self.client.get("/legal/ubuntu-pro-description/print").status_code,
            200,
        )

    def test_ubuntu_pro_description_print_with_sections(self):
        """
        When given the /legal/ubuntu-pro-description/print URL with sections,
        we should return a 200 status code
        """
        self.assertEqual(
            self.client.get(
                "/legal/ubuntu-pro-description/print"
                "?sections=introduction,support"
            ).status_code,
            200,
        )


class TestJujuVersion(unittest.TestCase):
    def setUp(self):
        """
        Set up Flask app for testing
        """
        app.testing = True
        self.client = app.test_client()
        # The /juju/latest.json response is cached, so the cache is cleared to
        # prevent leakage between tests.
        get_latest_versions.cache_clear()
        return super().setUp()

    @responses.activate
    def test_latest_release(self):
        """
        Check that the latest Juju and Juju Dashboard release versions are
        returned as JSON.
        """
        responses.get(
            "https://api.github.com/repos/canonical/"
            "juju-dashboard/releases/latest",
            json={
                "tag_name": "v1.2.3",
            },
        )
        responses.get(
            "https://api.github.com/repos/juju/juju/releases",
            json=[
                {
                    "tag_name": "v4.5.6",
                    "draft": False,
                    "prerelease": False,
                },
                {
                    "tag_name": "v4.5.5",
                    "draft": False,
                    "prerelease": False,
                },
                {
                    "tag_name": "v3.4.5",
                    "draft": False,
                    "prerelease": False,
                },
            ],
        )
        self.assertEqual(
            self.client.get("/juju/latest.json").json,
            {"dashboard": "v1.2.3", "juju": ["3.4.5", "4.5.6"]},
        )

    @responses.activate
    def test_latest_prerelease(self):
        """
        Check that drafts and pre-releases are ignored from the Juju and
        version response.
        """
        responses.get(
            "https://api.github.com/repos/canonical/"
            "juju-dashboard/releases/latest",
            json={
                "tag_name": "v1.2.3",
            },
        )
        responses.get(
            "https://api.github.com/repos/juju/juju/releases",
            json=[
                {
                    "tag_name": "v5.6.7",
                    "draft": True,
                    "prerelease": False,
                },
                {
                    "tag_name": "v4.5.6",
                    "draft": False,
                    "prerelease": True,
                },
                {
                    "tag_name": "v3.4.5",
                    "draft": False,
                    "prerelease": False,
                },
            ],
        )
        self.assertEqual(
            self.client.get("/juju/latest.json").json,
            {"dashboard": "v1.2.3", "juju": ["3.4.5"]},
        )
