import logging
import os
import unittest
from unittest.mock import MagicMock, patch

from webapp.app import app
from webapp import llms

logging.getLogger("talisker.context").disabled = True


def _make_response(status=200, content_type="text/markdown", body="content"):
    response = MagicMock()
    response.status_code = status
    response.content_type = content_type
    response.get_data.return_value = body
    return response


class TestLlmsHelpers(unittest.TestCase):
    def test_clean_collapses_whitespace(self):
        self.assertEqual(llms._clean("  a\n  b   c "), "a b c")
        self.assertEqual(llms._clean(None), "")

    def test_page_url(self):
        self.assertEqual(llms._page_url("/lxd"), "https://canonical.com/lxd")
        self.assertEqual(
            llms._page_url("/lxd", markdown=True),
            "https://canonical.com/lxd?format=md",
        )
        # Root and missing leading slash are normalised.
        self.assertEqual(llms._page_url("/"), "https://canonical.com/")
        self.assertEqual(llms._page_url("ceph"), "https://canonical.com/ceph")

    def test_heading_from_path(self):
        self.assertEqual(llms._heading_from_path("/legal"), "Legal")
        self.assertEqual(
            llms._heading_from_path("/open-source"), "Open Source"
        )

    def test_make_page_valid(self):
        node = {
            "name": "/lxd",
            "title": "LXD",
            "description": "Run\n containers",
        }
        self.assertEqual(
            llms._make_page(node),
            {"path": "/lxd", "title": "LXD", "description": "Run containers"},
        )

    def test_make_page_filters_non_content(self):
        # No title
        self.assertIsNone(llms._make_page({"name": "/x", "title": None}))
        # Excluded from sitemap
        self.assertIsNone(
            llms._make_page(
                {"name": "/x", "title": "X", "sitemap_exclude": True}
            )
        )
        # Noise paths (disallowed for AI crawlers in robots.txt)
        for path in ["/contact-us", "/foo/thank-you", "/careers/results"]:
            self.assertIsNone(
                llms._make_page({"name": path, "title": "T"}),
                f"{path} should be filtered",
            )

    def test_make_page_applies_overrides(self):
        node = {"name": "/events", "title": "Events", "description": ""}
        overrides = {"/events": {"description": "Meet us at conferences."}}
        page = llms._make_page(node, overrides)
        self.assertEqual(page["title"], "Events")
        self.assertEqual(page["description"], "Meet us at conferences.")

    def test_make_page_override_title_and_exclude(self):
        node = {"name": "/lxd", "title": "LXD", "description": "old"}
        # Title override
        self.assertEqual(
            llms._make_page(node, {"/lxd": {"title": "LXD containers"}})[
                "title"
            ],
            "LXD containers",
        )
        # Exclude override drops the page
        self.assertIsNone(llms._make_page(node, {"/lxd": {"exclude": True}}))

    def test_bullet_with_and_without_description(self):
        self.assertEqual(
            llms._bullet({"path": "/lxd", "title": "LXD", "description": "D"}),
            "- [LXD](https://canonical.com/lxd?format=md): D",
        )
        self.assertEqual(
            llms._bullet({"path": "/lxd", "title": "LXD", "description": ""}),
            "- [LXD](https://canonical.com/lxd?format=md)",
        )

    def test_link_bullet(self):
        self.assertEqual(
            llms._link_bullet(
                {"title": "Docs", "url": "https://x.com", "description": "D"}
            ),
            "- [Docs](https://x.com): D",
        )
        self.assertEqual(
            llms._link_bullet(
                {"title": "Docs", "url": "https://x.com", "description": ""}
            ),
            "- [Docs](https://x.com)",
        )


class TestLlmsExtraSections(unittest.TestCase):
    def _write_config(self, content):
        import tempfile

        handle = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)
        handle.write(content)
        handle.close()
        self.addCleanup(os.remove, handle.name)
        # _load_extra_sections joins cwd with this; an absolute path wins.
        patcher = patch.object(llms, "LLMS_CONFIG_FILE", handle.name)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_missing_file_returns_empty(self):
        with patch.object(llms, "LLMS_CONFIG_FILE", "/no/such/llms.yaml"):
            self.assertEqual(llms._load_extra_sections(), [])
            self.assertEqual(llms._load_overrides(), {})

    def test_load_overrides(self):
        self._write_config(
            """
overrides:
  /events:
    description: Meet us at conferences.
  /lxd:
    title: LXD containers
  /internal:
    exclude: true
  /bad:
    something: ignored
"""
        )
        overrides = llms._load_overrides()
        self.assertEqual(
            overrides["/events"], {"description": "Meet us at conferences."}
        )
        self.assertEqual(overrides["/lxd"], {"title": "LXD containers"})
        self.assertEqual(overrides["/internal"], {"exclude": True})
        # A no-op override normalises to an empty dict.
        self.assertEqual(overrides["/bad"], {})

    def test_parses_valid_sections(self):
        self._write_config(
            """
extra:
  - heading: Documentation
    links:
      - title: Ubuntu Server docs
        url: https://ubuntu.com/server/docs
        description: Official docs.
      - title: Discourse
        url: https://discourse.ubuntu.com/
"""
        )
        sections = llms._load_extra_sections()
        self.assertEqual(len(sections), 1)
        heading, links = sections[0]
        self.assertEqual(heading, "Documentation")
        self.assertEqual(
            links[0],
            {
                "title": "Ubuntu Server docs",
                "url": "https://ubuntu.com/server/docs",
                "description": "Official docs.",
            },
        )
        # Description is optional.
        self.assertEqual(links[1]["description"], "")

    def test_skips_invalid_entries(self):
        self._write_config(
            """
extra:
  - heading: Missing links
  - links:
      - title: No heading
        url: https://x.com
  - heading: Good
    links:
      - title: No url
      - url: https://only-url.com
      - title: Valid
        url: https://valid.com
"""
        )
        sections = llms._load_extra_sections()
        # Only the "Good" section with its single valid link survives.
        self.assertEqual(len(sections), 1)
        heading, links = sections[0]
        self.assertEqual(heading, "Good")
        self.assertEqual([link["title"] for link in links], ["Valid"])

    def test_empty_file_returns_empty(self):
        self._write_config("extra:\n")
        self.assertEqual(llms._load_extra_sections(), [])

    @patch("webapp.llms._load_extra_sections")
    def test_extra_sections_appear_in_llms_txt(self, mock_extra):
        mock_extra.return_value = [
            (
                "Documentation",
                [
                    {
                        "title": "Ubuntu Server docs",
                        "url": "https://ubuntu.com/server/docs",
                        "description": "Official docs.",
                    }
                ],
            )
        ]
        output = llms.generate_llms_txt()
        self.assertIn("## Documentation", output)
        self.assertIn(
            "- [Ubuntu Server docs]"
            "(https://ubuntu.com/server/docs): Official docs.",
            output,
        )
        # Curated sections render before the auto-generated page list.
        self.assertLess(
            output.index("## Documentation"), output.index("## Main pages")
        )


class TestLlmsSections(unittest.TestCase):
    def setUp(self):
        self.tree = {
            "name": "",
            "title": "Home",
            "description": "Welcome",
            "children": [
                {"name": "/consulting", "title": "Consulting", "children": []},
                {
                    "name": "/lxd",
                    "title": "LXD",
                    "description": "Containers",
                    "children": [
                        {
                            "name": "/lxd/install",
                            "title": "Install",
                            "children": [],
                        }
                    ],
                },
                # Section whose index page has no title -> heading from path.
                {
                    "name": "/legal",
                    "title": None,
                    "children": [
                        {
                            "name": "/legal/faq",
                            "title": "FAQ",
                            "children": [],
                        }
                    ],
                },
            ],
        }

    def test_build_sections_structure(self):
        sections = llms._build_sections(self.tree)
        headings = [heading for heading, _ in sections]

        # Main pages comes first and holds the home + top-level leaf pages.
        self.assertEqual(headings[0], "Main pages")
        main_paths = [p["path"] for p in sections[0][1]]
        self.assertEqual(main_paths, ["/", "/consulting"])

        # Sub-trees become their own sections.
        self.assertIn("LXD", headings)
        # Section with no index title falls back to a path-derived heading.
        self.assertIn("Legal", headings)

        lxd_pages = dict(sections)["LXD"]
        self.assertEqual(
            [p["path"] for p in lxd_pages], ["/lxd", "/lxd/install"]
        )


class TestLlmsFullGeneration(unittest.TestCase):
    @patch("webapp.llms._scan_tree")
    def test_skips_pages_that_fail_to_render(self, mock_scan):
        mock_scan.return_value = {
            "name": "",
            "title": None,
            "children": [
                {"name": "/good", "title": "Good", "children": []},
                {"name": "/bad", "title": "Bad", "children": []},
            ],
        }

        fake_client = MagicMock()
        fake_client.get.side_effect = [
            _make_response(body="# Good page"),
            _make_response(status=500, content_type="text/html"),
        ]
        fake_app = MagicMock()
        fake_app.test_client.return_value = fake_client

        output = llms.generate_llms_full_txt(fake_app)

        self.assertIn("# Good page", output)
        self.assertNotIn("Bad", output)
        # Markdown was requested against the canonical base URL.
        fake_client.get.assert_any_call(
            "/good?format=md", base_url=llms.BASE_URL
        )


def _llms_file_path(key):
    return os.path.join(os.getcwd(), llms.LLMS_FILES[key]["filename"])


class TestLlmsRoutes(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        # Start from a clean slate so GET exercises generate-on-missing.
        self._cleanup()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for key in llms.LLMS_FILES:
            path = _llms_file_path(key)
            if os.path.exists(path):
                os.remove(path)

    def test_llms_txt_generates_and_serves(self):
        # File is missing, so the GET generates it on demand...
        self.assertFalse(os.path.exists(_llms_file_path("llms.txt")))
        response = self.client.get("/llms.txt")
        body = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"], "text/plain; charset=utf-8"
        )
        self.assertTrue(body.startswith("# Canonical"))
        self.assertIn("## Main pages", body)
        self.assertIn("?format=md", body)
        # Noise pages are not advertised.
        self.assertNotIn("/contact-us?format=md", body)
        # ...and the result is now cached on disk for subsequent requests.
        self.assertTrue(os.path.exists(_llms_file_path("llms.txt")))
        self.assertEqual(self.client.get("/llms.txt").status_code, 200)

    @patch(
        "webapp.llms.generate_llms_full_txt",
        return_value="# Canonical\n\nfull content\n",
    )
    def test_llms_full_txt_served_from_disk(self, mock_generate):
        response = self.client.get("/llms-full.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Type"], "text/plain; charset=utf-8"
        )
        self.assertIn("full content", response.get_data(as_text=True))
        mock_generate.assert_called_once()

    def test_post_unauthorized(self):
        os.environ["LLMS_SECRET"] = "known-secret"
        response = self.client.post(
            "/llms.txt",
            headers={"Authorization": "Bearer wrong-secret"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "Unauthorized"})

    def test_post_authorized_regenerates(self):
        os.environ["LLMS_SECRET"] = "known-secret"
        response = self.client.post(
            "/llms.txt",
            headers={"Authorization": "Bearer known-secret"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully generated", response.get_json()["message"])
        self.assertTrue(os.path.exists(_llms_file_path("llms.txt")))


if __name__ == "__main__":
    unittest.main()
