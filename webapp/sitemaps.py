"""XML sitemap responses: the page lists and view functions behind
/sitemap.xml, /sitemap-links.xml, /careers/sitemap.xml,
/partners/sitemap.xml, and /knowledge/sitemap.xml. Routed from
webapp/app.py.
"""

from pathlib import Path

import flask

from webapp.careers import DEPARTMENT_LIST
from webapp.views import (
    get_file_last_modified,
    get_parent_last_modified,
    get_knowledge_sections,
)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

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

CAREERS_STATIC_SITEMAP_PAGES = [
    ("https://canonical.com/careers", "careers/index.html", "monthly"),
    (
        "https://canonical.com/careers/career-explorer",
        "careers/career-explorer.html",
        "monthly",
    ),
    ("https://canonical.com/careers/all", "careers/all.html", "weekly"),
    (
        "https://canonical.com/careers/hiring-process",
        "careers/hiring-process/index.html",
        "weekly",
    ),
    (
        "https://canonical.com/careers/company-culture/remote-work",
        "careers/company-culture/remote-work.html",
        "monthly",
    ),
    (
        "https://canonical.com/careers/company-culture/progression",
        "careers/company-culture/progression.html",
        "monthly",
    ),
    (
        "https://canonical.com/careers/company-culture/diversity",
        "careers/company-culture/diversity.html",
        "monthly",
    ),
    (
        "https://canonical.com/careers/company-culture/sustainability",
        "careers/company-culture/sustainability.html",
        "monthly",
    ),
]

PARTNERS_SITEMAP_PAGES = [
    ("https://canonical.com/partners", "partners/index.html"),
    (
        "https://canonical.com/partners/find-a-partner",
        "partners/find-a-partner.html",
    ),
    (
        "https://canonical.com/partners/become-a-partner",
        "partners/become-a-partner.html",
    ),
    (
        "https://canonical.com/partners/channel-and-reseller",
        "partners/channel-and-reseller.html",
    ),
    ("https://canonical.com/partners/desktop", "partners/desktop.html"),
    ("https://canonical.com/partners/gsi", "partners/gsi.html"),
    (
        "https://canonical.com/partners/ihv-and-oem",
        "partners/ihv-and-oem.html",
    ),
    (
        "https://canonical.com/partners/public-cloud",
        "partners/public-cloud.html",
    ),
    (
        "https://canonical.com/partners/iot-device",
        "partners/iot-device.html",
    ),
    ("https://canonical.com/partners/silicon", "partners/silicon/index.html"),
    (
        "https://canonical.com/partners/silicon/intel",
        "partners/silicon/intel/index.html",
    ),
    (
        "https://canonical.com/partners/executive-summit",
        "partners/executive-summit.html",
    ),
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
    pages = [
        {
            "url": url,
            "last_modified": get_file_last_modified(TEMPLATES_DIR / path),
            "changefreq": changefreq,
        }
        for url, path, changefreq in CAREERS_STATIC_SITEMAP_PAGES
    ]
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
        pages=pages,
        vacancies=greenhouse.get_vacancies(),
        departments=departments,
    )


def partners_sitemap():
    pages = [
        {
            "url": url,
            "last_modified": get_file_last_modified(TEMPLATES_DIR / path),
        }
        for url, path in PARTNERS_SITEMAP_PAGES
    ]

    return _xml_response("partners/sitemap.xml", pages=pages)


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
