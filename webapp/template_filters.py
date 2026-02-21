"""
Jinja2 template filters for the Canonical website.
"""

# Standard library
import hashlib
import re
import time
from urllib.parse import urlparse

# Third-party
import bleach
import markdown
from slugify import slugify


def convert_to_kebab(kebab_input):
    """Convert text to kebab-case format."""
    words = re.findall(
        r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", kebab_input
    )
    return "-".join(map(str.lower, words))


def get_nav_path(path):
    """Extract the first path segment for navigation."""
    short_path = ""
    split_path = path.split("/")
    if len(split_path) > 1:
        short_path = path.split("/")[1]
    return short_path


def get_secondary_nav_path(path):
    """Extract the second path segment for secondary navigation."""
    secondary_path = ""
    split_path = path.split("/")
    if len(split_path) > 2:
        secondary_path = path.split("/")[2]
    return secondary_path


def slug(text):
    """Convert text to a URL-friendly slug."""
    return slugify(text)


def markup(text):
    """Convert markdown text to HTML."""
    return markdown.markdown(text)


def allow_src(tag, name, value):
    """
    Helper function for filtered_html_tags.
    Validates allowed sources for iframe src attributes.
    """
    allowed_sources = ["www.youtube.com", "www.vimeo.com"]
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        return (not p.netloc) or p.netloc in allowed_sources
    return False


def filtered_html_tags(content):
    """
    Clean HTML content, allowing only safe tags and attributes.
    Removes empty paragraphs and sanitizes iframe sources.
    """
    content = content.replace("<p>&nbsp;</p>", "")
    allowed_tags = [
        "iframe",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "a",
        "strong",
        "ul",
        "ol",
        "li",
        "i",
        "em",
        "br",
    ]
    allowed_attributes = {"iframe": allow_src, "a": "href"}

    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
    )


def generate_image_id(text, prefix="image"):
    """
    Generate a unique ID from text using MD5 hash.
    Used for creating unique IDs for image captions.

    Args:
        text: Text to hash (typically the caption)
        prefix: Prefix for the ID (default: "image")

    Returns:
        String in format: {prefix}-{hash}
    """
    if not text:
        # Fallback for empty captions - use timestamp
        text = str(time.time())
    hash_value = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"{prefix}-{hash_value}"


def register_template_filters(app):
    """
    Register all custom template filters with the Flask app.

    Args:
        app: Flask application instance
    """
    app.template_filter()(convert_to_kebab)
    app.template_filter()(get_nav_path)
    app.template_filter()(get_secondary_nav_path)
    app.template_filter()(slug)
    app.template_filter()(markup)
    app.template_filter()(filtered_html_tags)
    app.template_filter()(generate_image_id)
