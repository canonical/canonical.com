"""Generate llms.txt and llms-full.txt for AI crawlers.

Both files follow the https://llmstxt.org/ convention:

- ``/llms.txt`` is a curated index of the site's main pages, each with a
  title, a link to its Markdown version (``?format=md``) and a short
  description.
- ``/llms-full.txt`` concatenates the full Markdown content of every page.

The page list, titles and descriptions are derived from the same template
tree used to build ``sitemap_tree.xml``
(``canonicalwebteam.directory_parser``), so these files stay in sync with the
templates automatically. The full page content reuses the existing
``?format=md`` Markdown rendering (``canonicalwebteam.markdown_response``).
"""

import logging
import os
import re
import tempfile

import canonicalwebteam.directory_parser as directory_parser
import flask
import yaml
from canonicalwebteam.flask_base.env import get_flask_env

logger = logging.getLogger(__name__)

BASE_URL = "https://canonical.com"
SITE_TITLE = "Canonical"
SITE_DESCRIPTION = (
    "Canonical makes open source secure, reliable and easy to use, providing "
    "support for Ubuntu and a portfolio of enterprise-grade technologies. "
    "Founded in 2004, Canonical operates globally with team members in over "
    "80 countries."
)

# Sections (top-level template directories) that are served by their own
# dynamic sitemaps, or are not content pages, and should not be walked here.
# Mirrors DYNAMIC_SITEMAPS in webapp/app.py plus the navigation partials.
EXCLUDE_PATHS = [
    "careers",
    "partners",
    "blog",
    "knowledge",
    "microk8s/docs",
    "dqlite/docs",
    "maas/docs",
    "tests",
    "navigation",
]

# Individual pages that are disallowed for AI crawlers in robots.txt
# (form/flow pages rather than content) and so are excluded from llms.txt.
NOISE_PATH_RE = re.compile(r"(contact-us|thank-you|/results)$")

# Writer-maintained file (repo root) with per-page overrides and extra curated
# link sections. In llms.txt the curated sections are rendered first (before
# the auto-discovered page lists); in llms-full.txt they follow the page
# content. See llms.yaml.
LLMS_CONFIG_FILE = "llms.yaml"


def _clean(text):
    """Collapse whitespace in a title or description to a single line."""
    return re.sub(r"\s+", " ", text or "").strip()


def _page_url(path, markdown=False):
    """Build an absolute canonical.com URL from a tree node path."""
    path = path or "/"
    if not path.startswith("/"):
        path = "/" + path
    url = BASE_URL + path
    if markdown:
        url += "?format=md"
    return url


def _make_page(node, overrides=None):
    """Return a page dict for *node*, or None if it is not a content page.

    *overrides* (from llms.yaml, keyed by path) can correct the title or
    description, or drop the page entirely via ``exclude``.
    """
    overrides = overrides or {}
    title = node.get("title")
    path = node.get("name") or "/"
    if not title or node.get("sitemap_exclude") or NOISE_PATH_RE.search(path):
        return None

    override = overrides.get(path, {})
    if override.get("exclude"):
        return None

    description = override.get("description")
    if description is None:
        description = node.get("description")
    return {
        "path": path,
        "title": _clean(override.get("title") or title),
        "description": _clean(description),
    }


def _heading_from_path(path):
    """Derive a readable section heading from a path (e.g. /legal -> Legal)."""
    segment = (path or "").rstrip("/").rsplit("/", 1)[-1]
    return segment.replace("-", " ").replace("_", " ").strip().title()


def _collect_pages(node, pages, overrides=None):
    """Depth-first collect every content page under *node*."""
    page = _make_page(node, overrides)
    if page:
        pages.append(page)
    for child in node.get("children", []):
        _collect_pages(child, pages, overrides)
    return pages


def _build_sections(tree, overrides=None):
    """Group the page tree into ordered (heading, [pages]) sections.

    Top-level directories with children become their own section; the home
    page and any standalone top-level pages are grouped under "Main pages".
    """
    main_pages = []
    sections = []

    # Home page (root index) and any top-level leaf pages.
    home = _make_page(tree, overrides)
    if home:
        main_pages.append(home)

    for child in tree.get("children", []):
        if child.get("children"):
            pages = _collect_pages(child, [], overrides)
            if pages:
                heading = _clean(child.get("title")) or _heading_from_path(
                    child.get("name")
                )
                sections.append((heading, pages))
        else:
            page = _make_page(child, overrides)
            if page:
                main_pages.append(page)

    if main_pages:
        sections.insert(0, ("Main pages", main_pages))
    return sections


def _scan_tree():
    """Scan the templates directory into a page tree."""
    templates_path = os.path.join(os.getcwd(), "templates")
    return directory_parser.scan_directory(
        templates_path, exclude_paths=EXCLUDE_PATHS
    )


def _bullet(page):
    """Render a single page as an llms.txt bullet."""
    line = f"- [{page['title']}]({_page_url(page['path'], markdown=True)})"
    if page["description"]:
        line += f": {page['description']}"
    return line


def _link_bullet(link):
    """Render a curated link (with an explicit URL) as a bullet."""
    line = f"- [{link['title']}]({link['url']})"
    if link["description"]:
        line += f": {link['description']}"
    return line


def _load_config():
    """Load and parse llms.yaml, returning a dict (empty if absent/invalid).

    The config is purely additive/corrective on top of auto-generation, so a
    missing or malformed file never breaks the generated output.
    """
    path = os.path.join(os.getcwd(), LLMS_CONFIG_FILE)
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as config_file:
            return yaml.safe_load(config_file) or {}
    except (OSError, yaml.YAMLError):
        logger.exception("Failed to read %s", LLMS_CONFIG_FILE)
        return {}


def _load_overrides(config=None):
    """Load per-page overrides from llms.yaml, keyed by page path.

    Each value may set ``title`` and/or ``description`` (to fix a weak or
    wrong auto-generated entry) or ``exclude: true`` (to drop the page). This
    is the "automatically generated and overridable" layer: the page list is
    still discovered automatically, but the docs team can correct entries in
    place without editing templates.

    Pass an already-parsed *config* to avoid re-reading the file.
    """
    if config is None:
        config = _load_config()
    overrides = {}
    for path, override in (config.get("overrides") or {}).items():
        if not isinstance(override, dict):
            continue
        normalised = {}
        if override.get("exclude"):
            normalised["exclude"] = True
        if override.get("title"):
            normalised["title"] = _clean(override.get("title"))
        if override.get("description") is not None:
            normalised["description"] = _clean(override.get("description"))
        overrides[path] = normalised
    return overrides


def _load_extra_sections(config=None):
    """Load curated extra link sections from llms.yaml.

    Returns a list of ``(heading, [links])`` tuples, where each link is a dict
    with ``title``, ``url`` and ``description``. Returns an empty list if the
    file is absent, empty or malformed — extras are purely additive, so a bad
    config never breaks the generated files.

    Pass an already-parsed *config* to avoid re-reading the file.
    """
    if config is None:
        config = _load_config()
    sections = []
    for section in config.get("extra") or []:
        heading = _clean(section.get("heading"))
        links = []
        for link in section.get("links") or []:
            title = _clean(link.get("title"))
            url = (link.get("url") or "").strip()
            if title and url:
                links.append(
                    {
                        "title": title,
                        "url": url,
                        "description": _clean(link.get("description")),
                    }
                )
        if heading and links:
            sections.append((heading, links))
    return sections


def generate_llms_txt():
    """Build the llms.txt index from the template tree."""
    config = _load_config()
    tree = _scan_tree()
    sections = _build_sections(tree, _load_overrides(config))

    lines = [f"# {SITE_TITLE}", "", f"> {SITE_DESCRIPTION}", ""]

    # Curated extra link sections from llms.yaml are rendered first, so the
    # docs team's high-value links keep priority and are not dropped by
    # context-limited crawlers that read from the top.
    for heading, links in _load_extra_sections(config):
        lines.append(f"## {heading}")
        lines.append("")
        lines.extend(_link_bullet(link) for link in links)
        lines.append("")

    for heading, pages in sections:
        lines.append(f"## {heading}")
        lines.append("")
        lines.extend(_bullet(page) for page in pages)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def generate_llms_full_txt(app):
    """Build llms-full.txt by rendering every page to Markdown in-process.

    Each page is fetched through the app's test client with ``?format=md`` so
    it reuses the existing HTML-to-Markdown conversion. Pages that fail to
    render (e.g. transient upstream errors) are skipped so a single failure
    never breaks the whole file.
    """
    config = _load_config()
    tree = _scan_tree()
    pages = _collect_pages(tree, [], _load_overrides(config))
    extra_sections = _load_extra_sections(config)

    client = app.test_client()
    parts = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
        "Full Markdown content of the main pages on canonical.com. "
        f"For the page index, see {BASE_URL}/llms.txt.",
    ]

    for page in pages:
        path = page["path"] or "/"
        try:
            response = client.get(f"{path}?format=md", base_url=BASE_URL)
        except Exception:
            logger.exception("Failed to render %s for llms-full.txt", path)
            continue

        if response.status_code != 200 or "markdown" not in (
            response.content_type or ""
        ):
            logger.warning(
                "Skipping %s in llms-full.txt (status %s)",
                path,
                response.status_code,
            )
            continue

        body = response.get_data(as_text=True).strip()
        if body:
            parts.append("")
            parts.append(body)

    # Curated extra link sections from llms.yaml.
    for heading, links in extra_sections:
        parts.append("")
        parts.append(f"## {heading}")
        parts.append("")
        parts.extend(_link_bullet(link) for link in links)

    return "\n".join(parts).rstrip() + "\n"


# Generated files are written to disk (like templates/sitemap_tree.xml) and
# served from there, so a regular GET never has to render every page. They are
# regenerated by an authenticated POST, triggered from CI on every push to
# main (see .github/workflows/llms.yaml). Keyed by the served path.
LLMS_FILES = {
    "llms.txt": {
        "filename": "templates/llms.txt",
        # Cheap to build: parses the template tree only.
        "generator": lambda app: generate_llms_txt(),
        "max_age": 60 * 60 * 6,  # 6 hours
    },
    "llms-full.txt": {
        "filename": "templates/llms-full.txt",
        # Expensive to build: renders every page to Markdown.
        "generator": lambda app: generate_llms_full_txt(app),
        "max_age": 60 * 60 * 24,  # 24 hours
    },
}


def build_llms_view(app, key):
    """Return a Flask view that serves (GET) or regenerates (POST) an
    llms file, mirroring the sitemap_tree.xml generate-on-POST pattern.
    """
    config = LLMS_FILES[key]
    file_path = os.path.join(os.getcwd(), config["filename"])

    def generate_file():
        content = config["generator"](app)
        # Write to a temp file in the same directory and atomically replace,
        # so a concurrent GET never reads a half-written file.
        directory = os.path.dirname(file_path) or "."
        fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(content)
            os.replace(tmp_path, file_path)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise
        logger.info("%s saved to %s", key, file_path)
        return content

    def serve_llms_file():
        # Regenerate with an authenticated POST (used by CI on deploy).
        if flask.request.method == "POST":
            expected_secret = get_flask_env("LLMS_SECRET")
            provided_secret = flask.request.headers.get(
                "Authorization", ""
            ).replace("Bearer ", "")

            if not expected_secret or provided_secret != expected_secret:
                logger.warning("Invalid secret provided for %s", key)
                return {"error": "Unauthorized"}, 401

            try:
                generate_file()
            except Exception as error:
                logger.exception("Failed to generate %s", key)
                return {"error": f"Could not generate {key}: {error}"}, 500

            return {"message": f"{key} successfully generated"}, 200

        # Generate on demand if the file is missing (e.g. fresh container).
        if not os.path.exists(file_path):
            try:
                generate_file()
            except Exception:
                logger.exception("Failed to generate %s", key)

        if not os.path.exists(file_path):
            return {"error": f"{key} not available"}, 503

        with open(file_path, "r") as f:
            content = f.read()

        response = flask.make_response(content)
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        response.headers["Cache-Control"] = (
            f"public, max-age={config['max_age']}"
        )
        return response

    return serve_llms_file
