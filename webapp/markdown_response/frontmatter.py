"""Extract metadata from HTML <head> into YAML frontmatter."""

import yaml
from bs4 import BeautifulSoup


def extract_frontmatter(html):
    """Parse HTML and return YAML frontmatter string from <head> meta tags.

    Returns a string like:
        ---
        title: Page Title
        description: Page description
        url: https://canonical.com/page
        ---
    """
    soup = BeautifulSoup(html, "html.parser")
    meta = {}

    # Title — strip " | Canonical" suffix
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        title = title_tag.string.strip()
        title = title.removesuffix(" | Canonical")
        title = title.removesuffix(" | Trusted open source for enterprises")
        title = title.strip()
        if title:
            meta["title"] = title

    # Description
    desc = _get_meta(soup, "description")
    if desc:
        meta["description"] = desc

    # URL
    url = _get_meta_property(soup, "og:url")
    if url:
        meta["url"] = url

    # Author
    author = _get_meta(soup, "author")
    if author and author != "Canonical Ltd":
        meta["author"] = author

    # Keywords
    keywords = _get_meta(soup, "keywords")
    if keywords:
        meta["keywords"] = keywords

    # Blog-specific: date and tags
    date = _get_meta_property(soup, "article:published_time")
    if date:
        meta["date"] = date

    tags = _get_meta_property(soup, "article:tag")
    if tags:
        meta["tags"] = tags

    if not meta:
        return ""

    frontmatter = yaml.dump(
        meta, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    return f"---\n{frontmatter}---\n"


def _get_meta(soup, name):
    """Get content from <meta name="..."> tag."""
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.get("content"):
        return tag["content"].strip()
    return None


def _get_meta_property(soup, prop):
    """Get content from <meta property="..."> tag."""
    tag = soup.find("meta", attrs={"property": prop})
    if tag and tag.get("content"):
        return tag["content"].strip()
    return None
