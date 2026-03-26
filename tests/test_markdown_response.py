import unittest
from webapp.markdown_response.frontmatter import extract_frontmatter
from webapp.markdown_response.converter import convert_html_to_markdown


class TestFrontmatter(unittest.TestCase):
    def test_extracts_title(self):
        html = """
        <html>
        <head>
            <title>What is Kubernetes | Canonical</title>
            <meta name="description" content="Learn about Kubernetes" />
            <meta property="og:url" content="https://canonical.com/blog/what-is-kubernetes" />
        </head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertIn("title: What is Kubernetes", result)
        self.assertNotIn("| Canonical", result)

    def test_extracts_description_and_url(self):
        html = """
        <html>
        <head>
            <title>Test Page | Canonical</title>
            <meta name="description" content="A test page" />
            <meta property="og:url" content="https://canonical.com/test" />
        </head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertIn("description: A test page", result)
        self.assertIn("url: https://canonical.com/test", result)

    def test_extracts_blog_specific_fields(self):
        html = """
        <html>
        <head>
            <title>Blog Post | Canonical</title>
            <meta name="description" content="A blog post" />
            <meta property="og:url" content="https://canonical.com/blog/post" />
            <meta name="author" content="Jane Doe" />
            <meta property="article:published_time" content="2025-06-15" />
            <meta property="article:tag" content="kubernetes" />
        </head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertIn("author: Jane Doe", result)
        self.assertIn("date: '2025-06-15'", result)
        self.assertIn("tags: kubernetes", result)

    def test_omits_missing_fields(self):
        html = """
        <html>
        <head>
            <title>Simple Page | Canonical</title>
        </head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertIn("title: Simple Page", result)
        self.assertNotIn("description:", result)
        self.assertNotIn("author:", result)
        self.assertNotIn("date:", result)
        self.assertNotIn("tags:", result)

    def test_frontmatter_has_delimiters(self):
        html = """
        <html>
        <head><title>Page | Canonical</title></head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertTrue(result.startswith("---\n"))
        self.assertTrue(result.endswith("\n---\n"))

    def test_strips_whitespace_in_description(self):
        html = """
        <html>
        <head>
            <title>Page | Canonical</title>
            <meta name="description" content="
                Multi line description with extra spaces
            " />
        </head>
        <body></body>
        </html>
        """
        result = extract_frontmatter(html)
        self.assertIn(
            "description: Multi line description with extra spaces", result
        )


class TestConverter(unittest.TestCase):
    def test_extracts_main_content(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <nav><a href="/">Home</a><a href="/about">About</a></nav>
            <div id="main-content">
                <h1>Hello World</h1>
                <p>This is the content.</p>
            </div>
            <footer><p>Copyright 2025</p></footer>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("# Hello World", result)
        self.assertIn("This is the content.", result)
        self.assertNotIn("Home", result)
        self.assertNotIn("About", result)
        self.assertNotIn("Copyright", result)

    def test_strips_script_and_style_tags(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content">
                <h1>Page</h1>
                <script>alert('hi')</script>
                <style>.foo { color: red; }</style>
                <p>Content here.</p>
            </div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("Content here.", result)
        self.assertNotIn("alert", result)
        self.assertNotIn(".foo", result)

    def test_strips_nav_and_noscript(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content">
                <nav><a href="/nav-link">Nav</a></nav>
                <noscript>Enable JS</noscript>
                <p>Real content.</p>
            </div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("Real content.", result)
        self.assertNotIn("Nav", result)
        self.assertNotIn("Enable JS", result)

    def test_strips_hidden_elements(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content">
                <p>Visible content.</p>
                <div class="u-hide">Hidden stuff</div>
                <a class="u-off-screen">Skip link</a>
            </div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("Visible content.", result)
        self.assertNotIn("Hidden stuff", result)
        self.assertNotIn("Skip link", result)

    def test_falls_back_to_body(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <h1>No main-content div</h1>
            <p>Body content.</p>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("# No main-content div", result)
        self.assertIn("Body content.", result)

    def test_collapses_excessive_blank_lines(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content">
                <h1>Title</h1>
                <br><br><br><br><br>
                <p>After many breaks.</p>
            </div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        # Should not have more than 2 consecutive newlines
        self.assertNotIn("\n\n\n\n", result)

    def test_custom_content_selector(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content"><p>Wrong div.</p></div>
            <div id="custom-content"><p>Right div.</p></div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(
            html, content_selector="#custom-content"
        )
        self.assertIn("Right div.", result)
        self.assertNotIn("Wrong div.", result)
