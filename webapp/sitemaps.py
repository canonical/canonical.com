"""XML sitemap responses: the page lists and view functions behind
/sitemap.xml, /sitemap-links.xml, /careers/sitemap.xml, and
/knowledge/sitemap.xml. Routed from webapp/app.py.

/partners and the static pages under /careers have no dedicated route
here -- they're discovered by the generic directory_parser-based
/sitemap_tree.xml (see webapp/app.py:build_sitemap_tree) instead, now
that its lastmod dates work (patched below).
"""

from pathlib import Path

import flask
from canonicalwebteam.directory_parser import app as directory_parser_app

from webapp.careers import DEPARTMENT_LIST
from webapp.views import (
    get_file_last_modified,
    get_parent_last_modified,
    get_knowledge_sections,
)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _directory_parser_last_modified(path):
    """Patches directory_parser's default lastmod lookup, which shells
    out to `git log` per file at request time and silently fails since
    production ships no .git. Reads our build-time manifest instead."""
    try:
        return get_file_last_modified(Path(path))
    except ValueError:
        return None


directory_parser_app.get_git_last_modified_time = (
    _directory_parser_last_modified
)

HOME_SITEMAP_PAGES = [
    ("https://canonical.com/", "index.html"),
    ("https://canonical.com/contact-us", "contact-us.html"),
    ("https://canonical.com/projects", "projects/index.html"),
    ("https://canonical.com/documentation", "documentation/index.html"),
    ("https://canonical.com/press-center", "press-center/index.html"),
    ("https://canonical.com/data", "data/index.html"),
    (
        "https://canonical.com/solutions/telco/5g-edge",
        "solutions/telco/5g-edge.html",
    ),
    (
        "https://canonical.com/solutions/telco/5g-core",
        "solutions/telco/5g-core.html",
    ),
    ("https://canonical.com/company", "company/index.html"),
    ("https://canonical.com/knowledge", "knowledge/index.html"),
]


def _xml_response(template, **context):
    xml_sitemap = flask.render_template(template, **context)
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


def index_sitemap():
    return _xml_response("sitemap-index.xml")


def home_sitemap():
    pages = [
        {
            "url": url,
            "last_modified": get_file_last_modified(TEMPLATES_DIR / path),
        }
        for url, path in HOME_SITEMAP_PAGES
    ]

    return _xml_response("sitemap-links.xml", pages=pages)


def careers_sitemap(greenhouse):
    departments = [
        {
            "slug": slug,
            "last_modified": get_file_last_modified(
                TEMPLATES_DIR / "careers" / f"{slug}.html"
            ),
        }
        for slug in DEPARTMENT_LIST
    ]

    return _xml_response(
        "careers/sitemap.xml",
        vacancies=greenhouse.get_vacancies(),
        departments=departments,
    )


def knowledge_sitemap():
    sections = get_knowledge_sections()
    last_modified = get_parent_last_modified(
        TEMPLATES_DIR / "knowledge" / "index.html",
        (s["last_modified"] for s in sections),
    )

    return _xml_response(
        "knowledge/sitemap.xml",
        sections=sections,
        last_modified=last_modified,
    )
