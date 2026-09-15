import unittest
from pathlib import Path
from unittest.mock import MagicMock

from webapp.wordpress import (
    WordPressError,
    fetch_page_raw_content,
    get_hero_from_page,
    map_hero,
    parse_blocks,
)

# Real content.raw captured from the WordPress editor for the demo page: it has
# an extra outer wrapper group and "--" encoded as \u002d\u002d inside the
# block-comment JSON. This is a static snapshot so tests run offline (no
# network or credentials); the running app fetches this live over HTTP instead.
WP_FIXTURE = (
    Path(__file__).parent / "fixtures" / "hero_content_raw_wp.html"
).read_text()


class TestParseBlocks(unittest.TestCase):
    def test_open_close_nesting_and_names(self):
        markup = (
            '<!-- wp:group {"className":"hero-layout--50-50"} -->'
            '<!-- wp:heading {"level":1} --><h1>T</h1><!-- /wp:heading -->'
            "<!-- wp:buttons -->"
            "<!-- wp:button --><a href=/a>A</a><!-- /wp:button -->"
            "<!-- wp:button --><a href=/b>B</a><!-- /wp:button -->"
            "<!-- /wp:buttons -->"
            "<!-- wp:image --><img src=/i.svg><!-- /wp:image -->"
            "<!-- /wp:group -->"
        )
        group = parse_blocks(markup)[0]
        self.assertEqual(group.name, "core/group")
        self.assertEqual(
            [b.name for b in group.inner_blocks],
            ["core/heading", "core/buttons", "core/image"],
        )
        buttons = group.inner_blocks[1]
        self.assertEqual(
            [b.name for b in buttons.inner_blocks],
            ["core/button", "core/button"],
        )

    def test_attrs_json_parsed(self):
        blocks = parse_blocks(
            '<!-- wp:heading {"level":1} --><h1>T</h1><!-- /wp:heading -->'
        )
        self.assertEqual(blocks[0].attrs.get("level"), 1)

    def test_void_block(self):
        blocks = parse_blocks('<!-- wp:spacer {"height":"20px"} /-->')
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].name, "core/spacer")
        self.assertEqual(blocks[0].attrs.get("height"), "20px")
        self.assertEqual(blocks[0].inner_blocks, [])

    def test_nested_json_attrs(self):
        # Real WP group blocks carry a nested "layout" object; the parser
        # must not truncate the JSON at the first closing brace.
        markup = (
            '<!-- wp:group {"className":"hero-layout--50-50",'
            '"layout":{"type":"constrained"}} -->\n'
            '<div class="wp-block-group hero-layout--50-50"></div>\n'
            "<!-- /wp:group -->"
        )
        blocks = parse_blocks(markup)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(
            blocks[0].attrs.get("className"), "hero-layout--50-50"
        )
        self.assertEqual(
            blocks[0].attrs.get("layout"), {"type": "constrained"}
        )

    def test_brace_inside_string_not_counted(self):
        markup = (
            '<!-- wp:paragraph {"content":"a } b"} -->'
            "x<!-- /wp:paragraph -->"
        )
        blocks = parse_blocks(markup)
        self.assertEqual(blocks[0].attrs.get("content"), "a } b")

    def test_editor_wrapper_group_is_nested(self):
        # The editor wraps hero content in an extra outer group.
        blocks = parse_blocks(WP_FIXTURE)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].name, "core/group")
        self.assertEqual(
            [b.name for b in blocks[0].inner_blocks], ["core/group"]
        )


class TestMapHero(unittest.TestCase):
    """Maps the real editor output (outer wrapper + \\u002d\\u002d classes)."""

    def setUp(self):
        self.hero = map_hero(parse_blocks(WP_FIXTURE))

    def test_maps_despite_outer_wrapper_group(self):
        self.assertIsNotNone(self.hero)
        self.assertEqual(
            self.hero["title_text"],
            "Take control of your large-scale deployments",
        )

    def test_subtitle_without_explicit_level(self):
        # The H2 has no "level" attribute; it must still be the subtitle.
        self.assertEqual(
            self.hero["subtitle_text"],
            "Enterprise-grade tooling, open source at heart",
        )

    def test_layout_decoded_from_escaped_class(self):
        self.assertEqual(self.hero["layout"], "50-50")

    def test_block_order_and_types(self):
        types = [b["type"] for b in self.hero["blocks"]]
        self.assertEqual(types, ["description", "cta-block", "image"])

    def test_description_block(self):
        description = next(
            b for b in self.hero["blocks"] if b["type"] == "description"
        )
        self.assertEqual(description["item"]["type"], "html")
        self.assertIn("Deploy, integrate", description["item"]["content"])

    def test_cta_block(self):
        cta = next(b for b in self.hero["blocks"] if b["type"] == "cta-block")[
            "item"
        ]
        self.assertEqual(cta["primary"]["content_html"], "Contact us")
        self.assertEqual(cta["primary"]["attrs"]["href"], "/contact-us")
        self.assertEqual(len(cta["secondaries"]), 1)
        self.assertEqual(
            cta["secondaries"][0]["attrs"]["href"],
            "https://github.com/canonical",
        )

    def test_image_block(self):
        image = next(b for b in self.hero["blocks"] if b["type"] == "image")[
            "item"
        ]
        self.assertEqual(
            image["attrs"]["src"],
            "https://assets.ubuntu.com/v1/d7c20674-JAAS-arch-diagram.svg",
        )
        self.assertEqual(image["attrs"]["alt"], "Architecture diagram")

    def test_image_aspect_ratio_and_dimensions(self):
        markup = (
            '<!-- wp:group {"className":"hero-layout--50-50"} -->'
            '<!-- wp:heading {"level":1} --><h1>T</h1><!-- /wp:heading -->'
            '<!-- wp:image {"className":"aspect--16-9"} -->'
            '<figure><img src="/a.svg" alt="alt" width="1848" '
            'height="933"/></figure><!-- /wp:image -->'
            "<!-- /wp:group -->"
        )
        image = next(
            b
            for b in map_hero(parse_blocks(markup))["blocks"]
            if b["type"] == "image"
        )["item"]
        self.assertEqual(image["aspect_ratio"], "16-9")
        self.assertEqual(image["attrs"]["width"], "1848")
        self.assertEqual(image["attrs"]["height"], "933")

    def test_no_title_returns_none(self):
        blocks = parse_blocks(
            "<!-- wp:group -->\n<div></div>\n<!-- /wp:group -->"
        )
        self.assertIsNone(map_hero(blocks))

    def test_signpost_image(self):
        markup = (
            '<!-- wp:group {"className":"hero-layout--25-75"} -->\n'
            '<!-- wp:heading {"level":1} -->\n<h1>Title</h1>\n'
            "<!-- /wp:heading -->\n"
            '<!-- wp:image {"className":"signpost"} -->\n'
            '<figure><img src="/sign.svg" alt="sign"/></figure>\n'
            "<!-- /wp:image -->\n"
            "<!-- /wp:group -->"
        )
        hero = map_hero(parse_blocks(markup))
        signposts = [
            b for b in hero["blocks"] if b["type"] == "signpost_image"
        ]
        self.assertEqual(len(signposts), 1)
        self.assertEqual(signposts[0]["item"]["attrs"]["src"], "/sign.svg")


class TestFetch(unittest.TestCase):
    def _session(self):
        session = MagicMock()
        response = MagicMock()
        response.json.return_value = {"content": {"raw": WP_FIXTURE}}
        response.raise_for_status.return_value = None
        session.get.return_value = response
        return session

    def test_fetch_calls_edit_context_with_auth(self):
        session = self._session()
        raw = fetch_page_raw_content(
            session, "https://wp.example.com/", "user", "pass", "42"
        )
        self.assertEqual(raw, WP_FIXTURE)
        session.get.assert_called_once()
        args, kwargs = session.get.call_args
        self.assertEqual(
            args[0], "https://wp.example.com/wp-json/wp/v2/pages/42"
        )
        self.assertEqual(kwargs["params"], {"context": "edit"})
        self.assertEqual(kwargs["auth"], ("user", "pass"))

    def test_get_hero_from_page(self):
        session = self._session()
        hero = get_hero_from_page(
            session, "https://wp.example.com", "user", "pass", "42"
        )
        self.assertEqual(
            hero["title_text"],
            "Take control of your large-scale deployments",
        )

    def test_missing_raw_raises_wordpress_error(self):
        session = MagicMock()
        response = MagicMock()
        # Unauthenticated ?context=edit returns rendered but no raw.
        response.json.return_value = {"content": {"rendered": "<p>x</p>"}}
        response.raise_for_status.return_value = None
        session.get.return_value = response
        with self.assertRaises(WordPressError):
            fetch_page_raw_content(
                session, "https://wp.example.com", "user", "pass", "42"
            )


if __name__ == "__main__":
    unittest.main()
