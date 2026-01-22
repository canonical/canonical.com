import unittest
from flask import Flask

from webapp.template_filters import (
    allow_src,
    convert_to_kebab,
    filtered_html_tags,
    generate_image_id,
    get_nav_path,
    get_secondary_nav_path,
    markup,
    register_template_filters,
    slug,
)


class TestConvertToKebab(unittest.TestCase):
    def test_converts_camelcase_to_kebab(self):
        self.assertEqual(convert_to_kebab("CamelCase"), "camel-case")
        self.assertEqual(convert_to_kebab("camelCase"), "camel-case")

    def test_converts_pascalcase_to_kebab(self):
        self.assertEqual(convert_to_kebab("PascalCase"), "pascal-case")

    def test_handles_acronyms(self):
        self.assertEqual(
            convert_to_kebab("HTTPSConnection"), "https-connection"
        )
        self.assertEqual(convert_to_kebab("XMLParser"), "xml-parser")

    def test_handles_numbers(self):
        self.assertEqual(convert_to_kebab("Ubuntu22.04"), "ubuntu-22-04")
        self.assertEqual(convert_to_kebab("Version2"), "version-2")

    def test_handles_already_kebab_case(self):
        self.assertEqual(convert_to_kebab("already-kebab"), "already-kebab")

    def test_handles_single_word(self):
        self.assertEqual(convert_to_kebab("word"), "word")
        self.assertEqual(convert_to_kebab("WORD"), "word")

    def test_handles_empty_string(self):
        self.assertEqual(convert_to_kebab(""), "")


class TestGetNavPath(unittest.TestCase):
    def test_extracts_first_segment(self):
        self.assertEqual(get_nav_path("/products/ubuntu"), "products")
        self.assertEqual(get_nav_path("/solutions/ai"), "solutions")

    def test_handles_single_segment(self):
        self.assertEqual(get_nav_path("/about"), "about")

    def test_handles_root_path(self):
        self.assertEqual(get_nav_path("/"), "")

    def test_handles_empty_string(self):
        self.assertEqual(get_nav_path(""), "")

    def test_handles_multiple_segments(self):
        self.assertEqual(get_nav_path("/a/b/c/d"), "a")

    def test_handles_trailing_slash(self):
        self.assertEqual(get_nav_path("/products/"), "products")


class TestGetSecondaryNavPath(unittest.TestCase):
    def test_extracts_second_segment(self):
        self.assertEqual(
            get_secondary_nav_path("/products/ubuntu/pro"), "ubuntu"
        )
        self.assertEqual(get_secondary_nav_path("/solutions/ai/ml"), "ai")

    def test_handles_no_second_segment(self):
        self.assertEqual(get_secondary_nav_path("/products"), "")
        self.assertEqual(get_secondary_nav_path("/"), "")

    def test_handles_exactly_two_segments(self):
        self.assertEqual(get_secondary_nav_path("/products/ubuntu"), "ubuntu")

    def test_handles_empty_string(self):
        self.assertEqual(get_secondary_nav_path(""), "")

    def test_handles_trailing_slash(self):
        self.assertEqual(get_secondary_nav_path("/products/ubuntu/"), "ubuntu")


class TestSlug(unittest.TestCase):
    def test_converts_to_slug(self):
        self.assertEqual(slug("Hello World"), "hello-world")
        self.assertEqual(slug("Ubuntu Pro"), "ubuntu-pro")

    def test_handles_special_characters(self):
        self.assertEqual(slug("Hello & World!"), "hello-world")
        self.assertEqual(slug("Test @ 123"), "test-123")

    def test_handles_multiple_spaces(self):
        self.assertEqual(slug("Multiple   Spaces"), "multiple-spaces")

    def test_handles_unicode(self):
        result = slug("Café")
        self.assertIsInstance(result, str)
        self.assertIn("caf", result.lower())

    def test_handles_empty_string(self):
        self.assertEqual(slug(""), "")


class TestMarkup(unittest.TestCase):
    def test_converts_markdown_to_html(self):
        result = markup("**bold**")
        self.assertIn("<strong>bold</strong>", result)

    def test_converts_headers(self):
        result = markup("# Header")
        self.assertIn("<h1>Header</h1>", result)

    def test_converts_links(self):
        result = markup("[Link](https://example.com)")
        self.assertIn('<a href="https://example.com">Link</a>', result)

    def test_converts_lists(self):
        result = markup("- Item 1\n- Item 2")
        self.assertIn("<ul>", result)
        self.assertIn("<li>Item 1</li>", result)

    def test_handles_empty_string(self):
        self.assertEqual(markup(""), "")

    def test_handles_plain_text(self):
        result = markup("Plain text")
        self.assertIn("Plain text", result)


class TestAllowSrc(unittest.TestCase):
    def test_allows_youtube_src(self):
        self.assertTrue(
            allow_src(
                None, "src", "https://www.youtube.com/embed/video123"
            )
        )

    def test_allows_vimeo_src(self):
        self.assertTrue(
            allow_src(None, "src", "https://www.vimeo.com/video123")
        )

    def test_allows_relative_src(self):
        self.assertTrue(allow_src(None, "src", "/local/video"))

    def test_blocks_other_domains(self):
        self.assertFalse(
            allow_src(None, "src", "https://evil.com/video")
        )

    def test_allows_alt_attribute(self):
        self.assertTrue(allow_src(None, "alt", "Video description"))

    def test_allows_height_attribute(self):
        self.assertTrue(allow_src(None, "height", "400"))

    def test_allows_width_attribute(self):
        self.assertTrue(allow_src(None, "width", "600"))

    def test_blocks_unknown_attributes(self):
        self.assertFalse(allow_src(None, "onclick", "alert()"))


class TestFilteredHtmlTags(unittest.TestCase):
    def test_removes_empty_paragraphs(self):
        result = filtered_html_tags("<p>&nbsp;</p><p>Content</p>")
        self.assertNotIn("<p>&nbsp;</p>", result)
        self.assertIn("<p>Content</p>", result)

    def test_allows_safe_tags(self):
        html = "<p>Text</p><strong>Bold</strong><em>Italic</em>"
        result = filtered_html_tags(html)
        self.assertIn("<p>Text</p>", result)
        self.assertIn("<strong>Bold</strong>", result)
        self.assertIn("<em>Italic</em>", result)

    def test_removes_dangerous_tags(self):
        html = "<script>alert('xss')</script><p>Safe</p>"
        result = filtered_html_tags(html)
        # Script tags removed but text content preserved (bleach behavior)
        self.assertNotIn("<script>", result)
        self.assertIn("<p>Safe</p>", result)

    def test_allows_links_with_href(self):
        html = '<a href="/page">Link</a>'
        result = filtered_html_tags(html)
        self.assertIn('<a href="/page">Link</a>', result)

    def test_allows_youtube_iframe(self):
        html = '<iframe src="https://www.youtube.com/embed/abc"></iframe>'
        result = filtered_html_tags(html)
        self.assertIn("<iframe", result)
        self.assertIn("youtube", result)

    def test_strips_disallowed_attributes(self):
        html = '<p onclick="alert()">Text</p>'
        result = filtered_html_tags(html)
        self.assertNotIn("onclick", result)
        self.assertIn("<p>Text</p>", result)

    def test_handles_headers(self):
        html = "<h2>Header 2</h2><h3>Header 3</h3>"
        result = filtered_html_tags(html)
        self.assertIn("<h2>Header 2</h2>", result)
        self.assertIn("<h3>Header 3</h3>", result)

    def test_handles_lists(self):
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        result = filtered_html_tags(html)
        self.assertIn("<ul>", result)
        self.assertIn("<li>Item 1</li>", result)

    def test_handles_line_breaks(self):
        html = "Line 1<br>Line 2"
        result = filtered_html_tags(html)
        self.assertIn("<br>", result)


class TestGenerateImageId(unittest.TestCase):
    def test_generates_consistent_id_for_same_text(self):
        id1 = generate_image_id("Test caption")
        id2 = generate_image_id("Test caption")
        self.assertEqual(id1, id2)

    def test_generates_different_ids_for_different_text(self):
        id1 = generate_image_id("Caption 1")
        id2 = generate_image_id("Caption 2")
        self.assertNotEqual(id1, id2)

    def test_uses_default_prefix(self):
        result = generate_image_id("Test")
        self.assertTrue(result.startswith("image-"))

    def test_uses_custom_prefix(self):
        result = generate_image_id("Test", prefix="caption")
        self.assertTrue(result.startswith("caption-"))

    def test_generates_8_char_hash(self):
        result = generate_image_id("Test caption")
        # Format: prefix-hash, where hash is 8 chars
        prefix, hash_part = result.rsplit("-", 1)
        self.assertEqual(len(hash_part), 8)

    def test_handles_empty_string(self):
        result = generate_image_id("")
        # Should use timestamp fallback
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("image-"))
        self.assertEqual(len(result.split("-")[1]), 8)

    def test_handles_unicode(self):
        result = generate_image_id("Café with émojis 🎉")
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("image-"))

    def test_deterministic_hash(self):
        # Same input should always produce same hash
        results = [generate_image_id("Test") for _ in range(5)]
        self.assertEqual(len(set(results)), 1)

    def test_handles_html_entities(self):
        result = generate_image_id("Image &copy; 2024")
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith("image-"))

    def test_handles_long_text(self):
        long_caption = "A" * 1000
        result = generate_image_id(long_caption)
        # Hash should still be 8 chars regardless of input length
        self.assertEqual(len(result.split("-")[1]), 8)


class TestRegisterTemplateFilters(unittest.TestCase):
    def test_registers_all_filters(self):
        app = Flask(__name__)
        register_template_filters(app)

        # Check that all filters are registered
        filter_names = [
            "convert_to_kebab",
            "get_nav_path",
            "get_secondary_nav_path",
            "slug",
            "markup",
            "filtered_html_tags",
            "generate_image_id",
        ]

        for filter_name in filter_names:
            self.assertIn(
                filter_name,
                app.jinja_env.filters,
                f"Filter '{filter_name}' not registered",
            )

    def test_filters_are_callable(self):
        app = Flask(__name__)
        register_template_filters(app)

        # Test that filters can be called
        env = app.jinja_env
        self.assertEqual(
            env.filters["convert_to_kebab"]("TestCase"), "test-case"
        )
        self.assertEqual(
            env.filters["get_nav_path"]("/products/ubuntu"), "products"
        )
        self.assertEqual(
            env.filters["slug"]("Hello World"), "hello-world"
        )

    def test_filters_work_in_templates(self):
        app = Flask(__name__)
        register_template_filters(app)

        # Test filter in actual template rendering
        with app.app_context():
            template = app.jinja_env.from_string("{{ text | slug }}")
            result = template.render(text="Hello World")
            self.assertEqual(result, "hello-world")

    def test_generate_image_id_filter_in_template(self):
        app = Flask(__name__)
        register_template_filters(app)

        with app.app_context():
            template = app.jinja_env.from_string(
                '{{ caption | generate_image_id("test") }}'
            )
            result = template.render(caption="Test Caption")
            self.assertTrue(result.startswith("test-"))
            self.assertEqual(len(result.split("-")[1]), 8)


if __name__ == "__main__":
    unittest.main()
