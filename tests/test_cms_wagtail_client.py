import unittest

import requests
import responses

from webapp.cms_wagtail.client import WagtailContent

API = "http://cms.test"
PAGE = {
    "id": 3,
    "meta": {"type": "website.MarketingPage", "seo_title": "", "search_description": "Fallback description"},
    "title": "Open source data",
    "meta_description": "Databases from Canonical",
    "meta_copydoc": "",
    "body_class": "is-paper",
    "body": [],
}


class WagtailContentTest(unittest.TestCase):
    def setUp(self):
        self.content = WagtailContent(requests.Session(), API + "/", site_host="canonical.localhost:8000")

    @responses.activate
    def test_resolves_a_path_without_following_the_redirect(self):
        responses.add(
            responses.GET, f"{API}/api/v2/pages/find/", status=302,
            headers={"Location": "http://canonical.localhost:8000/api/v2/pages/3/"},
        )
        responses.add(responses.GET, f"{API}/api/v2/pages/3/", json=PAGE)

        document = self.content.page_by_path("data/postgresql")

        self.assertEqual(document["title"], "Open source data")
        self.assertEqual(document["type"], "website.MarketingPage")
        self.assertEqual(document["meta"]["meta_description"], "Databases from Canonical")
        self.assertEqual(document["meta"]["body_class"], "is-paper")
        find, detail = responses.calls
        self.assertIn("html_path=%2Fdata%2Fpostgresql%2F", find.request.url)
        self.assertEqual(find.request.headers["Host"], "canonical.localhost:8000")
        self.assertEqual(detail.request.headers["Host"], "canonical.localhost:8000")
        self.assertTrue(detail.request.url.startswith(API))

    @responses.activate
    def test_root_path_normalises_to_a_single_slash(self):
        responses.add(
            responses.GET, f"{API}/api/v2/pages/find/", status=302,
            headers={"Location": f"{API}/api/v2/pages/3/"},
        )
        responses.add(responses.GET, f"{API}/api/v2/pages/3/", json=PAGE)
        responses.add(
            responses.GET, f"{API}/api/v2/pages/find/", status=302,
            headers={"Location": f"{API}/api/v2/pages/3/"},
        )
        responses.add(responses.GET, f"{API}/api/v2/pages/3/", json=PAGE)

        self.content.page_by_path("")
        self.content.page_by_path("/")

        find_urls = [call.request.url for call in responses.calls if "/find/" in call.request.url]
        self.assertEqual(len(find_urls), 2)
        for url in find_urls:
            self.assertIn("html_path=%2F", url)
            self.assertNotIn("html_path=%2F%2F", url)

    @responses.activate
    def test_an_unknown_path_is_none(self):
        responses.add(responses.GET, f"{API}/api/v2/pages/find/", status=404)
        self.assertIsNone(self.content.page_by_path("nope"))

    @responses.activate
    def test_seo_title_and_search_description_are_fallbacks(self):
        page = {**PAGE, "meta_description": "", "meta": {**PAGE["meta"], "seo_title": "Data | SEO"}}
        responses.add(
            responses.GET, f"{API}/api/v2/pages/find/", status=302,
            headers={"Location": f"{API}/api/v2/pages/3/"},
        )
        responses.add(responses.GET, f"{API}/api/v2/pages/3/", json=page)
        document = self.content.page_by_path("data")
        self.assertEqual(document["title"], "Data | SEO")
        self.assertEqual(document["heading"], "Open source data")
        self.assertEqual(document["meta"]["meta_description"], "Fallback description")

    @responses.activate
    def test_preview_is_fetched_by_token(self):
        responses.add(responses.GET, f"{API}/api/v2/page_preview/1/", json={**PAGE, "id": 0})
        document = self.content.preview("website.marketingpage", "tok-123")
        self.assertEqual(document["title"], "Open source data")
        self.assertIn("token=tok-123", responses.calls[0].request.url)
        self.assertIn("content_type=website.marketingpage", responses.calls[0].request.url)

    @responses.activate
    def test_an_expired_preview_is_none(self):
        responses.add(responses.GET, f"{API}/api/v2/page_preview/1/", status=404)
        self.assertIsNone(self.content.preview("website.marketingpage", "gone"))


if __name__ == "__main__":
    unittest.main()
