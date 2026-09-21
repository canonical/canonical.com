import unittest
from unittest.mock import patch

import requests
import responses

from webapp.app import app

API = "http://cms.test"
CONFIG = {"CMS_WAGTAIL_API_URL": API, "CMS_WAGTAIL_SITE_HOST": ""}
BODY = [
    {"type": "hero", "id": "1", "value": {
        "title": "Enterprise-grade data", "subtitle": "", "layout": "50/50",
        "description": "<p>Data flows <b>better</b>.</p>",
        "cta": {"primary_text": "Get in touch", "primary_url": "/contact-us"},
    }},
    {"type": "text_section", "id": "2", "value": {"heading": "Pricing", "body": "<p>From $25.</p>"}},
    {"type": "tiered_list", "id": "3", "value": {
        "title": "Why Canonical", "description": "", "cta": None,
        "items": [{"title": "Security", "description": "<p>Ten years.</p>"}],
    }},
    {"type": "highlight_list_section", "id": "4", "value": {"title": "Highlights", "items": ["Fast <fast>"]}},
    {"type": "data_list_section", "id": "5", "value": {
        "title": "Releases", "source": "supported_releases",
        "rows": [{"title": "24.04 LTS", "description": "Until 2029"}],
    }},
    {"type": "mystery_block", "id": "6", "value": {}},
]
PAGE = {
    "id": 3,
    "meta": {"type": "website.MarketingPage", "seo_title": "", "search_description": ""},
    "title": "Open source data",
    "meta_description": "Databases from Canonical",
    "meta_copydoc": "",
    "body_class": "is-paper",
    "body": BODY,
}


BODY_EXTRA = [
    {"type": "linked_logo_section", "id": "10", "value": {
        "title": "Databases", "layout": "25/75", "top_rule_variant": "default",
        "links": [{"href": "/data/mysql", "text": "MySQL", "label": "MySQL page",
                   "image_url": "https://assets.ubuntu.com/v1/m.png", "image_alt": "",
                   "image_width": 100, "image_height": 50}],
    }},
    {"type": "logo_section", "id": "11", "value": {
        "title": "Trusted by", "description": "<p>Because reasons.</p>",
        "logos": [{"image_url": "https://assets.ubuntu.com/v1/a.png", "alt": "A", "width": None, "height": None}],
    }},
    {"type": "tab_section", "id": "12", "value": {
        "title": "Why", "description": "<p>Because</p>",
        "tabs": [{"label": "One & only", "heading": "First <1>", "body": "<p>Body</p>",
                  "image_url": "", "image_alt": "", "link_text": "", "link_url": ""}],
    }},
    {"type": "equal_heights", "id": "13", "value": {
        "title": "Cards", "description": "", "cta": None,
        "items": [{"title": "Kept simple", "description": "<p>Straightforward pricing.</p>",
                   "image_url": "", "image_alt": ""}],
    }},
    {"type": "link_list_section", "id": "14", "value": {
        "title": "Resources",
        "groups": [{"heading": "Docs", "links": [{"href": "/docs/data", "text": "Data docs"}]}],
    }},
    {"type": "latest_blog", "id": "15", "value": {
        "heading": "Latest from our blog", "tag_ids": "", "layout": "4-blocks",
        "padding": "deep", "limit": 4, "excerpt_length": 200,
    }},
    {"type": "announcement", "id": "16", "value": {
        "criticality": "warning", "heading": "Heads up", "body": "<p>Soon</p>",
    }},
]
PAGE_EXTRA = {
    "id": 4,
    "meta": {"type": "website.MarketingPage", "seo_title": "", "search_description": ""},
    "title": "Extra blocks",
    "meta_description": "",
    "meta_copydoc": "",
    "body_class": "",
    "body": BODY_EXTRA,
}


def mock_page(page=PAGE, page_id=3):
    responses.add(
        responses.GET, f"{API}/api/v2/pages/find/", status=302,
        headers={"Location": f"{API}/api/v2/pages/{page_id}/"},
    )
    responses.add(responses.GET, f"{API}/api/v2/pages/{page_id}/", json=page)


class CmsWagtailViewsTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        patcher = patch.dict(app.config, CONFIG)
        patcher.start()
        self.addCleanup(patcher.stop)

    @responses.activate
    def test_a_cms_page_renders_in_the_canonical_shell(self):
        mock_page()
        response = self.client.get("/cms-wagtail/data")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Open source data | Canonical</title>", html)
        self.assertIn("Databases from Canonical", html)
        self.assertIn("is-paper", html)
        self.assertIn("Enterprise-grade data", html)
        self.assertIn("Data flows <b>better</b>.", html)
        self.assertIn('href="/contact-us"', html)
        self.assertIn("From $25.", html)
        self.assertIn("Ten years.", html)
        self.assertIn("24.04 LTS", html)

    @responses.activate
    def test_plain_fields_are_escaped(self):
        mock_page()
        html = self.client.get("/cms-wagtail/data").get_data(as_text=True)
        self.assertIn("Fast &lt;fast&gt;", html)
        self.assertNotIn("<fast>", html)

    @responses.activate
    def test_nested_paths_reach_the_api(self):
        mock_page()
        self.client.get("/cms-wagtail/data/postgresql/managed")
        self.assertIn("html_path=%2Fdata%2Fpostgresql%2Fmanaged%2F", responses.calls[0].request.url)

    @responses.activate
    def test_published_edits_are_not_cached(self):
        mock_page()
        response = self.client.get("/cms-wagtail/data")
        self.assertIn("no-cache", response.headers["Cache-Control"])

    @responses.activate
    def test_an_unknown_page_is_a_404(self):
        responses.add(responses.GET, f"{API}/api/v2/pages/find/", status=404)
        self.assertEqual(self.client.get("/cms-wagtail/nope").status_code, 404)

    @responses.activate
    def test_the_remaining_seven_block_types_render_their_content(self):
        mock_page(page=PAGE_EXTRA, page_id=4)
        html = self.client.get("/cms-wagtail/extra").get_data(as_text=True)
        self.assertIn("MySQL", html)  # linked_logo_section
        self.assertIn("Because reasons.", html)  # logo_section
        self.assertIn("First &lt;1&gt;", html)  # tab_section
        self.assertIn("Kept simple", html)  # equal_heights
        self.assertIn("Data docs", html)  # link_list_section
        self.assertIn('href="/docs/data"', html)  # link_list_section
        self.assertIn("Latest from our blog", html)  # latest_blog
        self.assertIn("Heads up", html)  # announcement

    @responses.activate
    def test_an_unreachable_cms_is_a_502(self):
        responses.add(
            responses.GET, f"{API}/api/v2/pages/find/",
            body=requests.ConnectionError("refused"),
        )
        self.assertEqual(self.client.get("/cms-wagtail/data").status_code, 502)

    @responses.activate
    def test_a_case_study_gets_its_own_hero_and_contact_section(self):
        study = {
            "id": 9,
            "meta": {"type": "website.CaseStudyPage", "seo_title": "", "search_description": ""},
            "title": "ESA launches on Ubuntu",
            "company_name": "ESA <agency>",
            "subtitle": "Space, on Ubuntu",
            "signpost_image_url": "https://assets.ubuntu.com/v1/abc-esa.png",
            "signpost_image_alt": 'ESA" onerror=alert(1) <x>',
            "meta_description": "", "meta_copydoc": "", "body_class": "is-paper",
            "body": [{"type": "text_section", "id": "1", "value": {"heading": "Challenge", "body": "<p>Scale.</p>"}}],
        }
        mock_page(study, page_id=9)
        html = self.client.get("/cms-wagtail/case-study/esa").get_data(as_text=True)
        self.assertIn("p-breadcrumbs", html)
        self.assertIn("ESA &lt;agency&gt;", html)
        self.assertIn("Space, on Ubuntu", html)
        self.assertIn("abc-esa.png", html)
        self.assertIn("Scale.", html)
        self.assertIn("Get in touch", html)
        self.assertNotIn('ESA" onerror=alert(1) <x>', html)
        self.assertIn("ESA&#34;", html)


if __name__ == "__main__":
    unittest.main()
