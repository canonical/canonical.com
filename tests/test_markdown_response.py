import unittest
from webapp.markdown_response.frontmatter import extract_frontmatter


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
