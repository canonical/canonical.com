import unittest
import flask
from webapp.markdown_response.frontmatter import extract_frontmatter
from webapp.markdown_response.converter import convert_html_to_markdown
from webapp.markdown_response import MarkdownResponse


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

    def test_strips_form_elements(self):
        html = """
        <html>
        <head><title>Test | Canonical</title></head>
        <body>
            <div id="main-content">
                <h1>Contact us</h1>
                <p>Get in touch with our team.</p>
                <form action="/submit" method="post">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" />
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
        """
        result = convert_html_to_markdown(html)
        self.assertIn("Contact us", result)
        self.assertIn("Get in touch with our team.", result)
        self.assertNotIn("Name", result)
        self.assertNotIn("Submit", result)
        self.assertNotIn("form", result.lower())

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


class TestMarkdownResponse(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)

        @self.app.route("/test")
        def test_page():
            return """
            <html>
            <head>
                <title>Test Page | Canonical</title>
                <meta name="description" content="A test page" />
                <meta property="og:url" content="https://canonical.com/test" />
            </head>
            <body>
                <nav><a href="/">Home</a></nav>
                <div id="main-content">
                    <h1>Test Page</h1>
                    <p>This is test content.</p>
                </div>
                <footer><p>Footer</p></footer>
            </body>
            </html>
            """

        MarkdownResponse(self.app)
        self.client = self.app.test_client()

    def test_normal_request_returns_html(self):
        response = self.client.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.content_type)
        self.assertIn(b"<h1>Test Page</h1>", response.data)

    def test_format_md_returns_markdown(self):
        response = self.client.get("/test?format=md")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/markdown", response.content_type)
        self.assertIn(b"# Test Page", response.data)
        self.assertIn(b"This is test content.", response.data)

    def test_format_md_has_frontmatter(self):
        response = self.client.get("/test?format=md")
        body = response.data.decode("utf-8")
        self.assertTrue(body.startswith("---\n"))
        self.assertIn("title: Test Page", body)
        self.assertIn("description: A test page", body)
        self.assertIn("url: https://canonical.com/test", body)

    def test_format_md_strips_navigation(self):
        response = self.client.get("/test?format=md")
        body = response.data.decode("utf-8")
        self.assertNotIn("Home", body)
        self.assertNotIn("Footer", body)

    def test_skips_non_html_responses(self):
        @self.app.route("/api")
        def api():
            return flask.jsonify({"key": "value"})

        response = self.client.get("/api?format=md")
        self.assertIn("application/json", response.content_type)

    def test_skips_non_200_responses(self):
        @self.app.route("/error")
        def error():
            return "<html><body>Not Found</body></html>", 404

        response = self.client.get("/error?format=md")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("text/markdown", response.content_type)

    def test_custom_content_selector(self):
        app2 = flask.Flask(__name__)

        @app2.route("/custom")
        def custom():
            return """
            <html>
            <head><title>Custom | Canonical</title></head>
            <body>
                <div id="wrapper"><p>Custom content.</p></div>
            </body>
            </html>
            """

        MarkdownResponse(app2, content_selector="#wrapper")
        client2 = app2.test_client()
        response = client2.get("/custom?format=md")
        self.assertIn(b"Custom content.", response.data)
