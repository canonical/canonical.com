"""Extract content from HTML and convert to Markdown."""

import re
from bs4 import BeautifulSoup
from markdownify import markdownify


DEFAULT_CONTENT_SELECTOR = "#main-content"
DEFAULT_STRIP_ELEMENTS = ["script", "style", "nav", "noscript"]
DEFAULT_STRIP_CLASSES = ["u-hide", "u-off-screen"]
STRIP_DATA_ATTR = "data-md-strip"


def convert_html_to_markdown(
    html,
    content_selector=DEFAULT_CONTENT_SELECTOR,
    strip_elements=None,
    strip_classes=None,
):
    """Convert an HTML page to clean Markdown.

    Extracts the content within the given CSS selector, strips unwanted
    elements, and converts the remaining HTML to Markdown.

    Elements with the data-md-strip attribute are always removed.
    """
    if strip_elements is None:
        strip_elements = DEFAULT_STRIP_ELEMENTS
    if strip_classes is None:
        strip_classes = DEFAULT_STRIP_CLASSES

    soup = BeautifulSoup(html, "html.parser")

    # Extract content area — fall back to <body> if selector not found
    content = soup.select_one(content_selector)
    if content is None:
        content = soup.find("body")
    if content is None:
        return ""

    # Strip unwanted elements by tag name
    for tag_name in strip_elements:
        for tag in content.find_all(tag_name):
            tag.decompose()

    # Strip elements with hidden/utility classes
    for cls in strip_classes:
        for tag in content.find_all(class_=cls):
            tag.decompose()

    # Strip elements marked with data-md-strip attribute
    for tag in content.find_all(attrs={STRIP_DATA_ATTR: True}):
        tag.decompose()

    # Convert to Markdown
    md = markdownify(str(content), heading_style="ATX", strip=["img"])

    # Strip trailing whitespace on each line first (handles "  \n" from <br>)
    md = "\n".join(line.rstrip() for line in md.splitlines())

    # Clean up: collapse excessive blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)

    return md.strip() + "\n"
