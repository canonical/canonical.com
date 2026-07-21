"""Build the LLM-friendly site index served at /llms.txt and /llms-full.txt.

``templates/llms.txt`` is hand-written and committed to git; it is the
source of truth for https://canonical.com/llms.txt (see
https://llmstxt.org/). ``llms.yaml`` (repo root) lets the docs team bolt on
extra curated link sections - e.g. product docs sites that live outside this
repo's own template tree - without touching the manual file directly.

``llms-full.txt`` concatenates the full Markdown content (``?format=md``) of
every same-site page linked from llms.txt. It is generated at build time
(``scripts/generate_llms.py``, run in the ``pack-rock`` job of
``.github/workflows/deploy.yaml``) because rendering every page is too slow
to redo on every app worker's cold start.
"""

import logging
import re

import yaml

logger = logging.getLogger(__name__)

BASE_URL = "https://canonical.com"

# Path prefixes served live from a Discourse instance - product docs and
# tutorials (canonicalwebteam.discourse Docs/Tutorials blueprints) or case
# studies/events (Engage pages, also backed by Discourse) - rather than
# rendered from this repo's own templates. See the blueprint registrations
# in webapp/app.py for each of these. llms-full.txt must not fetch them:
# the build environment has no Discourse API keys/allowlisting, and we
# don't want to scrape and redistribute that content anyway.
DISCOURSE_PATH_PREFIXES = (
    "/dqlite/docs",
    "/maas/docs",
    "/maas/tutorials",
    "/microk8s/docs",
    "/mir/docs",
    "/case-study",
    "/events",
)


def _clean(text):
    """Collapse whitespace in a title or description to a single line."""
    return re.sub(r"\s+", " ", text or "").strip()


def _load_extra_sections(llms_yaml_path):
    """Load curated extra link sections from llms.yaml.

    Returns a list of ``(heading, [links])`` tuples, where each link is a
    dict with ``title``, ``url`` and ``description``. Returns an empty list
    if the file is absent, empty or malformed - extras are purely additive,
    so a bad config never breaks the base llms.txt.
    """
    try:
        with open(llms_yaml_path) as config_file:
            config = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    except (OSError, yaml.YAMLError):
        logger.exception("Failed to read %s", llms_yaml_path)
        return []

    sections = []
    for section in (config or {}).get("extra") or []:
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


def _render_sections(sections):
    """Render ``(heading, [links])`` tuples as llms.txt markdown lines."""
    lines = []
    for heading, links in sections:
        lines.append(f"## {heading}")
        lines.append("")
        for link in links:
            line = f"- [{link['title']}]({link['url']})"
            if link["description"]:
                line += f": {link['description']}"
            lines.append(line)
        lines.append("")
    return lines


def _insert_after_section(base, heading, extra):
    """Insert *extra* markdown right after the named ``##`` section.

    Falls back to appending at the end if *heading* isn't found in *base*.
    """
    extra = extra.rstrip("\n")

    heading_match = re.search(
        rf"^## {re.escape(heading)}\s*$", base, re.MULTILINE
    )
    if not heading_match:
        stripped_base = base.rstrip("\n")
        return f"{stripped_base}\n\n{extra}\n"

    next_heading = re.search(
        r"^## ", base[heading_match.end() :], re.MULTILINE
    )
    if not next_heading:
        stripped_base = base.rstrip("\n")
        return f"{stripped_base}\n\n{extra}\n"

    insert_at = heading_match.end() + next_heading.start()
    before, after = base[:insert_at], base[insert_at:]
    return f"{before}{extra}\n\n{after}"


def build_llms_txt(llms_txt_path, llms_yaml_path):
    """Return the full /llms.txt body: manual base plus curated extras.

    Extra sections are inserted right after "Main pages" so they stay near
    the top, ahead of context-limited crawlers that read from the top.
    """
    with open(llms_txt_path) as llms_txt_file:
        base = llms_txt_file.read().rstrip("\n") + "\n"

    sections = _load_extra_sections(llms_yaml_path)
    if not sections:
        return base

    extra = "\n".join(_render_sections(sections)).rstrip("\n") + "\n"
    return _insert_after_section(base, "Main pages", extra)


_LINK_RE = re.compile(r"^-\s+\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)")


def _iter_links(llms_txt_content):
    """Yield (title, url) for every markdown link bullet in *content*."""
    for line in llms_txt_content.splitlines():
        match = _LINK_RE.match(line.strip())
        if match:
            yield match.group("title"), match.group("url")


def _is_renderable(url):
    """True if *url* is safe to fetch for llms-full.txt.

    Must be a ``?format=md`` link on this site (the manual llms.txt already
    only marks a link that way when it renders from our own templates) and
    must not fall under a Discourse-backed path - see DISCOURSE_PATH_PREFIXES.
    """
    if not url.startswith(BASE_URL) or "?format=md" not in url:
        return False
    path = url[len(BASE_URL) :].split("?", 1)[0]
    return not any(
        path == prefix or path.startswith(prefix + "/")
        for prefix in DISCOURSE_PATH_PREFIXES
    )


def build_llms_full_txt(app, llms_txt_content):
    """Render every renderable page linked from *llms_txt_content* to Markdown.

    Pages on other domains, without ``?format=md``, or served live from
    Discourse (product docs, tutorials, case studies, events) are skipped -
    see _is_renderable. A page that fails to render is skipped with a
    warning rather than failing the whole build.
    """
    client = app.test_client()
    parts = [
        "# Canonical",
        "",
        "> Full Markdown content of the pages listed in "
        f"{BASE_URL}/llms.txt. Product documentation, tutorials, case "
        "studies and events are omitted here (follow their links in "
        "llms.txt instead) since they are served live from Discourse.",
    ]

    seen_urls = set()
    for title, url in _iter_links(llms_txt_content):
        if url in seen_urls or not _is_renderable(url):
            continue
        seen_urls.add(url)

        path = url[len(BASE_URL) :]
        try:
            response = client.get(path, base_url=BASE_URL)
        except Exception:
            logger.exception("Skipping %s in llms-full.txt", path)
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
        if not body:
            continue

        parts.extend(
            ["", "---", "", f"# {title}", "", f"Source: {url}", "", body]
        )

    return "\n".join(parts).rstrip() + "\n"
