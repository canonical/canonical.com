import unittest

from markupsafe import Markup

from webapp.cms_wagtail.sections import cta_args, prepare_sections, rich

CTA = {
    "primary_text": "Get in touch", "primary_url": "/contact-us",
    "secondary_text": "", "secondary_url": "",
    "link_text": "Learn <more>", "link_url": "/data",
}


def one(block_type, value):
    sections = prepare_sections([{"type": block_type, "value": value, "id": "x"}])
    return sections[0]


class RichTextTest(unittest.TestCase):
    def test_scripts_and_handlers_are_stripped(self):
        html = rich('<p onclick="x()">Hi <b>there</b><script>alert(1)</script></p>')
        self.assertIsInstance(html, Markup)
        self.assertEqual(html, "<p>Hi <b>there</b>alert(1)</p>")

    def test_javascript_links_lose_their_href(self):
        self.assertNotIn("javascript", rich('<a href="javascript:alert(1)">x</a>'))


class CtaTest(unittest.TestCase):
    def test_buttons_are_escaped_and_the_link_gets_a_chevron(self):
        args = cta_args(CTA)
        self.assertEqual(args["primary"]["attrs"]["href"], "/contact-us")
        self.assertEqual(args["secondaries"], [])
        self.assertEqual(args["link"]["content_html"], "Learn &lt;more&gt;&nbsp;&rsaquo;")

    def test_a_missing_cta_is_empty(self):
        self.assertEqual(cta_args(None), {"primary": {}, "secondaries": [], "link": {}})


class PrepareSectionsTest(unittest.TestCase):
    def test_unknown_blocks_are_dropped(self):
        self.assertEqual(prepare_sections([{"type": "mystery", "value": {}, "id": "1"}]), [])
        self.assertEqual(prepare_sections(None), [])

    def test_hero_builds_description_and_cta_blocks(self):
        macro = one("hero", {
            "title": "Data<br>solutions<script>", "subtitle": "A & B", "layout": "50/50",
            "description": "<p>Run <b>PostgreSQL</b></p>", "cta": CTA,
        })["macro"]
        self.assertEqual(macro["title"], "Data<br>solutions")
        self.assertEqual(macro["subtitle"], "A &amp; B")
        self.assertEqual([block["type"] for block in macro["blocks"]], ["description", "cta-block"])
        self.assertEqual(macro["blocks"][0]["item"], {"type": "html", "content": "<p>Run <b>PostgreSQL</b></p>"})

    def test_hero_signpost_image_comes_first(self):
        macro = one("hero", {
            "title": "PostgreSQL", "layout": "25/75",
            "signpost_image_url": "https://assets.ubuntu.com/v1/abc-pg.png",
            "signpost_image_alt": "", "signpost_image_width": 200, "signpost_image_height": 200,
        })["macro"]
        self.assertEqual(macro["blocks"][0]["type"], "signpost_image")
        attrs = macro["blocks"][0]["item"]["attrs"]
        self.assertIn("abc-pg.png", attrs["src"])
        self.assertEqual(attrs["width"], "200")

    def test_an_image_without_dimensions_still_renders(self):
        macro = one("logo_section", {
            "title": "Trusted by", "description": "",
            "logos": [{"image_url": "https://assets.ubuntu.com/v1/a.png", "alt": "A", "width": None, "height": None}],
        })["macro"]
        logo = macro["blocks"][0]["item"]["logos"][0]
        self.assertEqual(logo, {"src": "https://assets.ubuntu.com/v1/a.png", "alt": "A"})

    def test_tabs_carry_heading_body_image_and_link(self):
        macro = one("tab_section", {
            "title": "Why", "description": "<p>Because</p>",
            "tabs": [
                {"label": "One & only", "heading": "First <1>", "body": "<p>Body</p>",
                 "image_url": "https://assets.ubuntu.com/v1/t.png", "image_alt": "T",
                 "link_text": "More", "link_url": "/more"},
                {"label": "Two", "heading": "Second", "body": "<p>B2</p>",
                 "image_url": "", "image_alt": "", "link_text": "", "link_url": ""},
            ],
        })["macro"]
        first, second = macro["tabs"]
        self.assertEqual(first["tab_html"], "One &amp; only")
        self.assertEqual(first["type"], "basic-section")
        self.assertEqual([item["type"] for item in first["item"]["items"]], ["description", "image", "cta-block"])
        self.assertEqual(
            first["item"]["items"][0]["item"]["content"],
            '<h3 class="p-heading--5">First &lt;1&gt;</h3><p>Body</p>',
        )
        self.assertEqual([item["type"] for item in second["item"]["items"]], ["description"])

    def test_equal_heights_items(self):
        macro = one("equal_heights", {
            "title": "Cards", "description": "", "cta": None,
            "items": [
                {"title": "A & B", "description": "<p>d</p>", "image_url": "https://assets.ubuntu.com/v1/c.png", "image_alt": "C"},
                {"title": "", "description": "<p>e</p>", "image_url": "", "image_alt": ""},
            ],
        })["macro"]
        self.assertEqual(macro["items"][0]["title_text"], "A &amp; B")
        self.assertIn("<img", macro["items"][0]["image_html"])
        self.assertEqual(macro["items"][1]["image_html"], "")

    def test_linked_logos(self):
        macro = one("linked_logo_section", {
            "title": "Databases", "layout": "25/75", "top_rule_variant": "default",
            "links": [{"href": "/data/mysql", "text": "MySQL", "label": "MySQL page",
                       "image_url": "https://assets.ubuntu.com/v1/m.png", "image_alt": "",
                       "image_width": 100, "image_height": 50}],
        })["macro"]
        self.assertEqual(macro["links"][0]["image_attrs"], {
            "src": "https://assets.ubuntu.com/v1/m.png", "alt": "", "width": "100", "height": "50", "class": "",
        })

    def test_latest_blog_ids_come_from_the_heading(self):
        macro = one("latest_blog", {"heading": "Latest from our blog", "tag_ids": "", "layout": "4-blocks",
                                     "padding": "deep", "limit": 4, "excerpt_length": 200})["macro"]
        self.assertEqual(macro["container_id"], "latest-blog-latest-from-our-blog-articles")
        self.assertEqual(macro["template_id"], "latest-blog-latest-from-our-blog-template")

    def test_announcement_maps_to_a_vanilla_notification(self):
        macro = one("announcement", {"criticality": "warning", "heading": "Heads up", "body": "<p>Soon</p>"})["macro"]
        self.assertEqual(macro["modifier"], "caution")

    def test_value_only_blocks_pass_through(self):
        section = one("data_list_section", {"title": "Releases", "source": "supported_releases",
                                             "rows": [{"title": "24.04", "description": "2029"}]})
        self.assertEqual(section["macro"], {})
        self.assertEqual(section["value"]["rows"][0]["title"], "24.04")


if __name__ == "__main__":
    unittest.main()
