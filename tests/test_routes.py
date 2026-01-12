import logging
import responses
import unittest

from vcr_unittest import VCRTestCase
from webapp.app import app, get_latest_versions


logging.getLogger("talisker.context").disabled = True


class TestRoutes(VCRTestCase):
    def _get_vcr_kwargs(self):
        """
        This removes the authorization header
        from VCR so we don't record auth parameters
        """
        return {"filter_headers": ["Authorization"]}

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
