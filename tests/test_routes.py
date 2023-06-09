import logging

from vcr_unittest import VCRTestCase
from webapp.app import app


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

    def test_working_here_pages(self):
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
            self.client.get("/careers/sustainability").status_code, 200
        )

    def test_invalid_careers_department(self):
        """
        When given the URL of an invalid careers department,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/careers/foo").status_code, 404)

    def test_careers_progression(self):
        """
        When given the URL of careers progression page,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get("/careers/progression").status_code, 200
        )

    def test_partners_detail_pages(self):
        """
        When given the URL of a valid parters detail page,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get("/partners/ihv-and-oem").status_code, 200
        )

    def test_not_found(self):
        """
        When given a non-existent URL,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/not-found-url").status_code, 404)

    def test_company_culture(self):
        """
        When given the URL of company culture page,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get("/careers/company-culture").status_code, 200
        )

    def test_diversity(self):
        """
        When given the URL of careers diversity page,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get("/careers/company-culture/diversity").status_code,
            200,
        )
