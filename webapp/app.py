# Standard library
import calendar
import datetime
import gzip
import hashlib
import json
import logging
import math
import os
import re
from http.client import responses
from pathlib import Path
from typing import List
from urllib.parse import parse_qs, urlencode, urlparse

import bleach
import canonicalwebteam.directory_parser as directory_parser
import flask
import markdown
import yaml

# Packages
from canonicalwebteam import image_template
from canonicalwebteam.blog import BlogAPI, BlogViews, build_blueprint
from canonicalwebteam.discourse import (
    DiscourseAPI,
    DocParser,
    Docs,
    EngagePages,
    TutorialParser,
    Tutorials,
)
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.flask_base.env import get_flask_env
from canonicalwebteam.form_generator import FormGenerator
from canonicalwebteam.search import build_search_view
from canonicalwebteam.templatefinder import TemplateFinder
from jinja2 import ChoiceLoader, FileSystemLoader
from requests.exceptions import HTTPError
from slugify import slugify

# Local
from webapp.views import json_asset_query
from webapp.application import application
from webapp.canonical_cla.views import (
    canonical_cla_api_github_login,
    canonical_cla_api_github_logout,
    canonical_cla_api_launchpad_login,
    canonical_cla_api_launchpad_logout,
    canonical_cla_api_proxy,
)
from webapp.greenhouse import Greenhouse, Harvest
from webapp.handlers import init_handlers
from webapp.navigation import (
    build_navigation,
    get_current_page_bubble,
    split_list,
)
from webapp.openapi_parser import parse_openapi, read_yaml_from_url
from webapp.partners import Partners
from webapp.recaptcha import load_recaptcha_config, verify_recaptcha
from webapp.requests_session import get_requests_session
from webapp.static_data import homepage_featured_products
from webapp.utils.juju_doc_search import (
    DOMAIN_INFO,
    process_and_sort_results,
    search_all_docs,
)

logger = logging.getLogger(__name__)

# Sitemaps that are already generated and don't need to be updated.
# Can be seen on sitemap_index.xml
DYNAMIC_SITEMAPS = [
    "careers",
    "partners",
    "blog",
]

# Web tribe websites custom search ID
search_engine_id = "adb2397a224a1fe55"

app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

# Load env variables after the app is initialized
CHARMHUB_DISCOURSE_API_KEY = os.getenv("CHARMHUB_DISCOURSE_API_KEY")
CHARMHUB_DISCOURSE_API_USERNAME = os.getenv("CHARMHUB_DISCOURSE_API_USERNAME")

RECAPTCHA_CONFIG = load_recaptcha_config()
RECAPTCHA_SITE_KEY = RECAPTCHA_CONFIG.get("site_key")
if not RECAPTCHA_SITE_KEY:
    logger.error("RECAPTCHA_SITE_KEY is missing!")


# ChoiceLoader attempts loading templates from each path in successive order
directory_parser_templates = (
    Path(directory_parser.__file__).parent / "templates"
)
loader = ChoiceLoader(
    [
        FileSystemLoader("templates"),
        FileSystemLoader("node_modules/vanilla-framework/templates/"),
        FileSystemLoader("static/js/modules/vanilla-framework/"),
        FileSystemLoader(str(directory_parser_templates)),
    ]
)

# Loader supplied to jinja_loader overwrites default jinja_loader
app.jinja_loader = loader

charmhub_discourse_api = DiscourseAPI(
    base_url="https://discourse.charmhub.io/",
    session=get_requests_session(),
    api_key=CHARMHUB_DISCOURSE_API_KEY,
    api_username=CHARMHUB_DISCOURSE_API_USERNAME,
    get_topics_query_id=2,
)
search_session = get_requests_session()
discourse_session = get_requests_session()

app.register_blueprint(application, url_prefix="/careers/application")


# Prepare forms
form_template_path = "shared/forms/form-template.html"
form_loader = FormGenerator(app, form_template_path)
form_loader.load_forms()


def _group_by_department(harvest, vacancies):
    """
    Return a dictionary of departments by slug,
    where each department will have a new
    "vacancies" property of all the vacancies in
    that department
    """

    all_departments = harvest.get_departments()
    vacancies_by_department = {}

    departments_by_slug = {}

    for department in all_departments:
        departments_by_slug[department.slug] = department

    for vacancy in vacancies:
        for department in vacancy.departments:
            slug = department.slug

            if slug not in vacancies_by_department:
                vacancies_by_department[slug] = departments_by_slug[slug]
                vacancies_by_department[slug].vacancies = [vacancy]
            else:
                vacancies_by_department[slug].vacancies.append(vacancy)

    # Add departments with no vacancies
    for dept in departments_by_slug:
        slug = departments_by_slug[dept].slug
        if slug not in vacancies_by_department:
            vacancies_by_department[slug] = departments_by_slug[slug]
            vacancies_by_department[slug].vacancies = {}

    return vacancies_by_department


def _get_sorted_departments(greenhouse, harvest):
    departments = _group_by_department(harvest, greenhouse.get_vacancies())

    sort_order = [
        "engineering",
        "support-engineering",
        "marketing",
        "web-and-design",
        "project-management",
        "commercial-operations",
        "product",
        "sales",
        "finance",
        "people",
        "administration",
        "legal",
        "alliances-and-channels",
    ]

    sorted = {slug: departments[slug] for slug in sort_order}
    remaining_slugs = set(departments.keys()).difference(sort_order)
    remaining = {slug: departments[slug] for slug in remaining_slugs}
    sorted_departments = {**sorted, **remaining}

    return sorted_departments


def _get_all_departments(greenhouse, harvest) -> tuple:
    """
    Refactor for careers search section
    """
    all_departments = (
        _group_by_department(harvest, greenhouse.get_vacancies()),
    )

    dept_list = [
        {"slug": "engineering", "icon": "84886ac6-Engineering.svg"},
        {
            "slug": "support-engineering",
            "icon": "df08c7f2-Support Engineering.svg",
        },
        {"slug": "marketing", "icon": "27b93be4-Marketing.svg"},
        {"slug": "web-and-design", "icon": "b200e162-design.svg"},
        {
            "slug": "project-management",
            "icon": "0f64ee5c-Project Management.svg",
        },
        {"slug": "commercial-operations", "icon": "1f84f8c7-Operations.svg"},
        {"slug": "product", "icon": "d5341dfa-Product.svg"},
        {"slug": "sales", "icon": "2dc1ceb1-Sales.svg"},
        {"slug": "finance", "icon": "8b2110ea-finance.svg"},
        {"slug": "people", "icon": "01ff5233-Human Resources.svg"},
        {"slug": "administration", "icon": "a42f5ab5-Admin.svg"},
        {"slug": "legal", "icon": "4e54c36b-Legal.svg"},
        {
            "slug": "alliances-and-channels",
            "icon": "46a968ed-no%20bg%20hand%20&%20fingers-new.svg",
        },
    ]

    departments_overview = []

    for vacancy in all_departments:
        for dept in dept_list:
            if vacancy[dept["slug"]]:
                if vacancy[dept["slug"]].vacancies:
                    count = len(vacancy[dept["slug"]].vacancies)
                else:
                    count = 0
                name = vacancy[dept["slug"]].name
                slug = vacancy[dept["slug"]].slug
                icon = dept["icon"]

                departments_overview.append(
                    {
                        "name": name,
                        "count": count,
                        "slug": slug,
                        "icon": icon,
                    }
                )

    return all_departments, departments_overview


sentry = app.extensions["sentry"]

init_handlers(app, sentry)


@app.route("/")
def index():
    context = {
        "featured_products": homepage_featured_products,
    }

    return flask.render_template("index.html", **context)


@app.route("/sitemap.xml")
def index_sitemap():
    xml_sitemap = flask.render_template("sitemap-index.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["-Control"] = "public, max-age=43200"

    return response


@app.route("/sitemap-links.xml")
def home_sitemap():
    xml_sitemap = flask.render_template("sitemap-links.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


app.add_url_rule("/asset/<file_name>", view_func=json_asset_query)


# OpenStack resources blog section
# tag_ids:
# openstack - 1327
def render_openstack_blogs():
    blogs = BlogViews(
        api=BlogAPI(session=get_requests_session()),
        excluded_tags=[3184, 3265, 3408, 3960, 4491, 3599],
        tag_ids=[1327],
        per_page=4,
        blog_title="OpenStack blogs",
    )
    openstack_articles = blogs.get_index()["articles"]
    sorted_articles = sorted(openstack_articles, key=lambda x: x["date"])
    return flask.render_template(
        "/openstack/resources.html", blogs=sorted_articles
    )


app.add_url_rule("/openstack/resources", view_func=render_openstack_blogs)


with open("navigation.yaml") as nav_file:
    navigation = yaml.load(nav_file.read(), Loader=yaml.FullLoader)
app.add_url_rule(
    "/search",
    "search",
    build_search_view(
        app=app,
        session=search_session,
        template_path="search.html",
        search_engine_id=search_engine_id,
        featured=navigation,
    ),
)


@app.route("/secure-boot-master-ca.crl")
def secure_boot():
    return flask.send_from_directory(
        "../static/files", "secure-boot-master-ca.crl"
    )


# Career departments
@app.route("/careers/results")
def handle_careers_results():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return careers_results(greenhouse, harvest)


@app.route("/juju/docs/search", methods=["GET"])
def search_docs():
    """Main search function that fetches and ranks documentation results."""
    query = flask.request.args.get("q", "").strip()
    if not query:
        return flask.redirect("/juju/docs")

    results = search_all_docs(query)
    sorted_results = process_and_sort_results(results, query)

    return flask.render_template(
        "juju/docs/search.html",
        query=query,
        sorted_results=sorted_results,
        domain_info=DOMAIN_INFO,
    )


def careers_results(greenhouse, harvest):
    vacancies = []

    core_skills = flask.request.args.get("core-skills", "").split(",")
    vacancies = greenhouse.get_vacancies_by_skills(core_skills)
    vacancies_by_department = _group_by_department(harvest, vacancies)

    context = {
        "all_departments": _group_by_department(
            harvest, greenhouse.get_vacancies()
        ),
        "vacancies": vacancies,
        "vacancies_by_department": vacancies_by_department,
        "recaptcha_site_key": RECAPTCHA_SITE_KEY,
    }

    return flask.render_template("careers/results.html", **context)


@app.route("/careers/sitemap.xml")
def handle_careers_sitemap():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return careers_sitemap(greenhouse, harvest)


def careers_sitemap(greenhouse, harvest):
    context = {
        "vacancies": greenhouse.get_vacancies(),
        "departments": harvest.get_departments(),
    }

    xml_sitemap = flask.render_template("careers/sitemap.xml", **context)
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


@app.route("/careers/feed")
def handle_careers_rss():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        return careers_rss(greenhouse)


def careers_rss(greenhouse):
    context = {"vacancies": greenhouse.get_vacancies()}

    xml_sitemap = flask.render_template("careers/rss.xml", **context)
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route(
    "/careers/<regex('[0-9]+'):job_id>",
    methods=["GET", "POST"],
    defaults={"job_title": None},
)
@app.route(
    "/careers/<regex('[0-9]+'):job_id>/<job_title>", methods=["GET", "POST"]
)
def handle_job_details(job_id, job_title):
    """
    job_title is not used, but is included in the route to avoid
    breaking existing links
    """
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return job_details(session, greenhouse, harvest, job_id)


def job_details(session, greenhouse, harvest, job_id):
    context = {
        "bleach": bleach,
        "recaptcha_site_key": RECAPTCHA_SITE_KEY,
    }

    try:
        # Greenhouse job board API (get_vacancy) doesn't show inactive roles
        context["job"] = harvest.get_job_post(job_id)
        job_post = greenhouse.get_vacancy(job_id)
        context["job"]["content"] = job_post.content
    except HTTPError as error:
        if error.response.status_code == 404:
            logger.exception(
                f"requesting details for non-existing job post {job_id=}"
            )
            flask.abort(404)
        else:
            raise error

    if flask.request.method == "POST":
        recaptcha_token = flask.request.form.get("recaptcha_token")
        recaptcha_passed = verify_recaptcha(
            session, recaptcha_token, "JOB_APPLY"
        )
        if not recaptcha_passed:
            context["message"] = {
                "type": "negative",
                "title": "Verification failed",
                "text": (
                    "Oops! We couldn't verify you're human. Please try again."
                ),
            }
            return flask.render_template("/careers/job-detail.html", **context)

        response = greenhouse.submit_application(
            flask.request.form, flask.request.files, job_id
        )
        if response.status_code == 200:
            return flask.render_template("/careers/thank-you.html", **context)

        else:
            logger.error(
                f"submit application error {response.status_code=} {job_id=}"
            )
            context["message"] = {
                "type": "negative",
                "title": f"Error {response.status_code}",
                "text": f"{response.reason}. Please try again!",
            }

    return flask.render_template("/careers/job-detail.html", **context)


@app.route("/careers/career-explorer")
def start_career():
    return flask.render_template(
        "/careers/career-explorer.html",
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/roles.json")
def handle_roles():
    """
    API endpoint for _navigation to consume
    roles by department section with the up to date roles.
    """
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return roles(greenhouse, harvest)


def roles(greenhouse, harvest):
    all_departments, departments_overview = _get_all_departments(
        greenhouse, harvest
    )
    return flask.jsonify(departments_overview)


@app.route("/careers")
def handle_careers_index():
    """
    Create a dictionary containing number of roles, slug
    and department name for a given department
    """
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return careers_index(greenhouse, harvest)


def careers_index(greenhouse, harvest):
    all_departments, departments_overview = _get_all_departments(
        greenhouse, harvest
    )

    return flask.render_template(
        "/careers/index.html",
        all_departments=all_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        departments_overview=departments_overview,
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/all")
def handle_all_careers():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return all_careers(greenhouse, harvest)


def all_careers(greenhouse, harvest):
    sorted_departments = _get_sorted_departments(greenhouse, harvest)

    return flask.render_template(
        "/careers/all.html",
        sorted_departments=sorted_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/hiring-process")
def hiring_process():
    return flask.render_template(
        "careers/hiring-process/index.html",
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


# Company culture pages
@app.route("/careers/company-culture")
def culture():
    return flask.render_template(
        "careers/company-culture/index.html",
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/company-culture/progression")
def handle_careers_progression():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return careers_progression(greenhouse, harvest)


def careers_progression(greenhouse, harvest):
    all_departments, departments_overview = _get_all_departments(
        greenhouse, harvest
    )

    return flask.render_template(
        "/careers/company-culture/progression.html",
        all_departments=all_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        departments_overview=departments_overview,
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/company-culture/diversity")
def handle_diversity():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return diversity(greenhouse, harvest)


def diversity(greenhouse, harvest):
    context = {
        "all_departments": _group_by_department(
            harvest, greenhouse.get_vacancies()
        ),
        "recaptcha_site_key": RECAPTCHA_SITE_KEY,
    }
    context["department"] = None
    return flask.render_template(
        "careers/company-culture/diversity.html", **context
    )


@app.route("/careers/company-culture/remote-work")
@app.route("/careers/company-culture/sustainability")
def handle_working_here_pages():
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        return working_here_pages(greenhouse)


def working_here_pages(greenhouse):
    sprint_locations = [
        [{"lat": 51.53910042435768, "lng": -0.1416575585467801}, "London"],
        [{"lat": -33.876169534561576, "lng": 18.382182743342554}, "Cape Town"],
        [{"lat": 55.67473557077814, "lng": 12.602819433367}, "Copenhagen"],
        [{"lat": 50.09169724226367, "lng": 14.37895031427894}, "Prague"],
        [{"lat": 50.142222694420674, "lng": 8.614639914385569}, "Frankfurt"],
        [{"lat": 45.50800862995117, "lng": -73.58280686860392}, "Montreal"],
        [{"lat": 43.69252498079002, "lng": -79.35691360946339}, "Toronto"],
        [{"lat": 45.76429262112831, "lng": 4.835301390987176}, "Lyon"],
        [{"lat": 56.94768919486784, "lng": 24.10684305711006}, "Riga"],
        [{"lat": 52.07521864310495, "lng": 4.30832253022489}, "The Hague"],
        [{"lat": 40.41680094106089, "lng": -3.703487758724201}, "Madrid"],
        [{"lat": 49.28246559657245, "lng": -123.11863290828228}, "Vancouver"],
    ]

    return flask.render_template(
        f"{flask.request.path}.html",
        sprint_locations=sprint_locations,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


@app.route("/careers/<department_slug>")
def handle_department_group(department_slug):
    with get_requests_session() as session:
        greenhouse = Greenhouse.from_session(session)
        harvest = Harvest.from_session(session)
        return department_group(greenhouse, harvest, department_slug)


def department_group(greenhouse, harvest, department_slug):
    departments = _get_sorted_departments(greenhouse, harvest)

    if department_slug not in departments:
        flask.abort(404)

    department = departments[department_slug]

    # format edge case slugs
    formatted_slug = ""
    if " & " in department.name:
        formatted_slug = department.name.replace(" & ", "+%26+")
    elif " " in department.name:
        formatted_slug = department.name.replace(" ", "+")

    featured_jobs = [job for job in department.vacancies if job.featured]
    fast_track_jobs = [job for job in department.vacancies if job.fast_track]

    templates = []

    # Generate list of templates in the /templates/careers folder,
    # and remove the .html suffix
    for template in os.listdir("./templates/careers"):
        if template.endswith(".html"):
            template = template[:-5]
        templates.append(template)

    return flask.render_template(
        "careers/base.html",
        department=department,
        sorted_departments=departments,
        featured_jobs=featured_jobs,
        fast_track_jobs=fast_track_jobs,
        formatted_slug=formatted_slug,
        templates=templates,
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
    )


# Partners
@app.route("/partners/find-a-partner")
def handle_find_a_partner():
    with get_requests_session() as session:
        partners_api = Partners(session)
        return find_a_partner(partners_api)


def find_a_partner(partners_api):
    partners = sorted(
        partners_api.get_partner_list(), key=lambda item: item["name"]
    )

    partners_length = len(partners)

    return flask.render_template(
        "/partners/find-a-partner.html",
        partners=partners,
        partners_length=partners_length,
    )


@app.route("/partners/channel-and-reseller")
@app.route("/partners/desktop")
@app.route("/partners/gsi")
@app.route("/partners/ihv-and-oem")
@app.route("/partners/public-cloud")
@app.route("/partners/iot-device")
@app.route("/partners/silicon")
@app.route("/partners/iot-device")
def handle_partner_details():
    with get_requests_session() as session:
        partners_api = Partners(session)
        return partner_details(partners_api)


def partner_details(partners_api):
    partners = partners_api._get(
        partners_api.partner_page_map[flask.request.path.split("/")[2]]
    )

    if flask.request.path == "/partners/silicon":
        template_path = "/partners/silicon/index.html"
    else:
        template_path = f"{flask.request.path}.html"

    return flask.render_template(template_path, partners=partners)


@app.route("/partners/sitemap.xml")
def partners_sitemap():
    xml_sitemap = flask.render_template("partners/sitemap.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


# Blog
class BlogView(flask.views.View):
    def __init__(self, blog_views):
        self.blog_views = blog_views


class PressCentre(BlogView):
    def dispatch_request(self):
        page_param = flask.request.args.get("page", default=1, type=int)
        category_param = flask.request.args.get(
            "category", default="", type=str
        )
        context = self.blog_views.get_group(
            "canonical-announcements", page_param, category_param
        )

        return flask.render_template("press-centre/index.html", **context)


class BlogSitemapIndex(BlogView):
    def dispatch_request(self):
        with get_requests_session() as session:
            response = session.get(
                "https://admin.insights.ubuntu.com/sitemap_index.xml",
                timeout=15,
            )

            xml = response.text.replace(
                "https://admin.insights.ubuntu.com/",
                "https://canonical.com/blog/sitemap/",
            )
            xml = re.sub(r"<\?xml-stylesheet.*\?>", "", xml)

            response = flask.make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response


class BlogSitemapPage(BlogView):
    def dispatch_request(self, slug):
        with get_requests_session() as session:
            response = session.get(
                f"https://admin.insights.ubuntu.com/{slug}.xml",
                timeout=15,
            )

            if response.status_code == 404:
                return flask.abort(404)

            xml = response.text.replace(
                "https://admin.insights.ubuntu.com/",
                "https://canonical.com/blog/",
            )
            xml = re.sub(r"<\?xml-stylesheet.*\?>", "", xml)

            response = flask.make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response


blog_views = BlogViews(
    api=BlogAPI(session=get_requests_session()),
    excluded_tags=[3184, 3265, 3599],
    per_page=11,
)

app.add_url_rule(
    "/blog/sitemap.xml",
    view_func=BlogSitemapIndex.as_view("sitemap", blog_views=blog_views),
)
app.add_url_rule(
    "/blog/sitemap/<regex('.+'):slug>.xml",
    view_func=BlogSitemapPage.as_view("sitemap_page", blog_views=blog_views),
)
app.add_url_rule(
    "/press-centre",
    view_func=PressCentre.as_view("press_centre", blog_views=blog_views),
)
app.register_blueprint(build_blueprint(blog_views), url_prefix="/blog")


# Template finder
template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.context_processor
def inject_today_date():
    return {"current_year": datetime.date.today().year}


def get_countries_list() -> List[dict]:
    """
    Get a list of countries in a standard format
    """
    from pycountry import countries

    countries = [
        {
            "alpha2": country.alpha_2,
            "name": getattr(country, "common_name", country.name),
        }
        for country in list(countries)
    ]
    return sorted(countries, key=lambda x: x["name"])


@app.context_processor
def utility_processor():
    return {
        "image": image_template,
        "get_countries_list": get_countries_list,
    }


# Blog pagination
def modify_query(params):
    query_params = parse_qs(
        flask.request.query_string.decode("utf-8"), keep_blank_values=True
    )
    query_params.update(params)

    return urlencode(query_params, doseq=True)


def descending_years(end_year):
    now = datetime.datetime.now()
    return range(now.year, end_year, -1)


def months_list(year):
    months = []
    now = datetime.datetime.now()
    for i in range(1, 13):
        date = datetime.date(year, i, 1)
        if date < now.date():
            months.append({"name": date.strftime("%b"), "number": i})
    return months


def month_name(string):
    month = int(string)
    return calendar.month_name[month]


# Template context
@app.context_processor
def context():
    return {
        "modify_query": modify_query,
        "descending_years": descending_years,
        "months_list": months_list,
        "month_name": month_name,
        "get_current_page_bubble": get_current_page_bubble,
        "build_navigation": build_navigation,
        "split_list": split_list,
        "canonical_cla_api_url": os.getenv("CANONICAL_CLA_API_URL"),
    }


@app.template_filter()
def convert_to_kebab(kebab_input):
    words = re.findall(
        r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", kebab_input
    )

    return "-".join(map(str.lower, words))


@app.template_filter()
def get_nav_path(path):
    short_path = ""
    split_path = path.split("/")
    if len(split_path) > 1:
        short_path = path.split("/")[1]
    return short_path


@app.template_filter()
def get_secondary_nav_path(path):
    secondary_path = ""
    split_path = path.split("/")
    if len(split_path) > 2:
        secondary_path = path.split("/")[2]
    return secondary_path


@app.template_filter()
def slug(text):
    return slugify(text)


@app.template_filter()
def markup(text):
    return markdown.markdown(text)


@app.template_filter()
def filtered_html_tags(content):
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


def allow_src(tag, name, value):
    allowed_sources = ["www.youtube.com", "www.vimeo.com"]
    if name in ("alt", "height", "width"):
        return True
    if name == "src":
        p = urlparse(value)
        return (not p.netloc) or p.netloc in allowed_sources
    return False


# Data Platform Spark on K8s docs
data_spark_k8s_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=8963,
        url_prefix="/data/docs/spark/k8s",
    ),
    document_template="/data/docs/spark/k8s/document.html",
    url_prefix="/data/docs/spark/k8s",
    blueprint_name="data-docs-spark-k8s",
)
app.add_url_rule(
    "/data/docs/spark/k8s/search",
    "data-docs-spark-k8s-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/spark/k8s",
        template_path="/data/docs/spark/k8s/search-results.html",
    ),
)
data_spark_k8s_docs.init_app(app)

# Data Platform MySQL on IAAS docs
data_mysql_iaas_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=9925,
        url_prefix="/data/docs/mysql/iaas",
    ),
    document_template="/data/docs/mysql/iaas/document.html",
    url_prefix="/data/docs/mysql/iaas",
    blueprint_name="data-docs-mysql-iaas",
)
app.add_url_rule(
    "/data/docs/mysql/iaas/search",
    "data-docs-mysql-iaas-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/mysql/iaas",
        template_path="/data/docs/mysql/iaas/search-results.html",
    ),
)
data_mysql_iaas_docs.init_app(app)

# Data Platform MySQL on K8s docs
data_mysql_k8s_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=9680,
        url_prefix="/data/docs/mysql/k8s",
    ),
    document_template="/data/docs/mysql/k8s/document.html",
    url_prefix="/data/docs/mysql/k8s",
    blueprint_name="data-docs-mysql-k8s",
)
app.add_url_rule(
    "/data/docs/mysql/k8s/search",
    "data-docs-mysql-k8s-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/mysql/k8s",
        template_path="/data/docs/mysql/k8s/search-results.html",
    ),
)
data_mysql_k8s_docs.init_app(app)

# Data Platform MongoDB on IaaS docs
data_mongodb_iaas_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=12461,
        url_prefix="/data/docs/mongodb/iaas",
    ),
    document_template="/data/docs/mongodb/iaas/document.html",
    url_prefix="/data/docs/mongodb/iaas",
    blueprint_name="data-docs-mongodb-iaas",
)
app.add_url_rule(
    "/data/docs/mongodb/iaas/search",
    "data-docs-mongodb-vm-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/mongodb/iaas",
        template_path="/data/docs/mongodb/iaas/search-results.html",
    ),
)
data_mongodb_iaas_docs.init_app(app)

# Data Platform MongoDB on K8s docs
data_mongodb_k8s_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=10265,
        url_prefix="/data/docs/mongodb/k8s",
    ),
    document_template="/data/docs/mongodb/k8s/document.html",
    url_prefix="/data/docs/mongodb/k8s",
    blueprint_name="data-docs-mongodb-k8s",
)
app.add_url_rule(
    "/data/docs/mongodb/k8s/search",
    "data-docs-mongodb-k8s-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/mongodb/k8s",
        template_path="/data/docs/mongodb/k8s/search-results.html",
    ),
)
data_mongodb_k8s_docs.init_app(app)

# Data Platform OpenSearch on IaaS docs
data_opensearch_iaas_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=9729,
        url_prefix="/data/docs/opensearch/iaas",
    ),
    document_template="/data/docs/opensearch/iaas/document.html",
    url_prefix="/data/docs/opensearch/iaas",
    blueprint_name="data-docs-opensearch-iaas",
)
app.add_url_rule(
    "/data/docs/opensearch/iaas/search",
    "data-docs-opensearch-iaas-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/opensearch/iaas",
        template_path="/data/docs/opensearch/iaas/search-results.html",
    ),
)
data_opensearch_iaas_docs.init_app(app)


# Data Platform index docs
data_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=10863,
        url_prefix="/data/docs",
    ),
    document_template="/data/docs/document.html",
    url_prefix="/data/docs/",
    blueprint_name="data_docs",
)

data_docs.init_app(app)


dqlite_docs = Docs(
    parser=DocParser(
        api=DiscourseAPI(
            base_url="https://discourse.dqlite.io/",
            session=discourse_session,
        ),
        index_topic_id=34,
        url_prefix="/dqlite/docs",
    ),
    document_template="/dqlite/docs/document.html",
    url_prefix="/dqlite/docs",
    blueprint_name="dqlite_docs",
)

app.add_url_rule(
    "/dqlite/docs/search",
    "dqlite-docs-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/dqlite/docs",
        template_path="/dqlite/docs/search-results.html",
    ),
)

dqlite_docs.init_app(app)

MAAS_DISCOURSE_API_KEY = os.getenv("MAAS_DISCOURSE_API_KEY")
MAAS_DISCOURSE_API_USERNAME = os.getenv("MAAS_DISCOURSE_API_USERNAME")


maas_url_prefix = "/maas/docs"
maas_docs = Docs(
    parser=DocParser(
        api=DiscourseAPI(
            base_url="https://discourse.maas.io/",
            session=discourse_session,
            get_topics_query_id=2,
        ),
        index_topic_id=6662,
        url_prefix=maas_url_prefix,
        tutorials_index_topic_id=1289,
        tutorials_url_prefix="/maas",
    ),
    document_template="maas/docs/document.html",
    url_prefix=maas_url_prefix,
)


maas_docs.init_app(app)


app.add_url_rule(
    "/maas/docs/search",
    "maas-docs-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/maas/docs",
        template_path="/maas/docs/search-result.html",
    ),
)


@app.route("/maas/docs/api")
def maas_docs_api():
    """
    Show the MAAS API reference page
    """
    # Fetch the OpenAPI definition from GitHub and parse it
    definition_url = (
        "https://raw.githubusercontent.com"
        "/canonical/maas-openapi-yaml/main/openapi.yaml"
    )
    definition = read_yaml_from_url(
        definition_url, session=get_requests_session()
    )
    openapi = parse_openapi(definition)

    # Inject the OpenAPI responses into the template
    with open("templates/maas/docs/_api.html", "r") as f:
        template_content = f.read()
    rendered_body_html = flask.render_template_string(
        template_content, openapi=openapi, responses=responses
    )

    # Mock an API response, and manually call the parsers
    document = {
        "title": "MAAS API",
        "body_html": rendered_body_html,
        "updated": "unknown, this document is generated dynamically",
        "topic_path": "api",
    }
    maas_docs.parser.parse()
    navigations = maas_docs.parser.navigations
    maas_docs.parser.navigation = maas_docs.parser._generate_navigation(
        navigations, ""
    )

    response = flask.make_response(
        flask.render_template(
            "maas/docs/document.html",
            document=document,
            nav_items=maas_docs.parser.navigation["nav_items"],
            navigation=maas_docs.parser.navigation,
        )
    )

    # Cache for 1 day
    response.headers["Cache-Control"] = "public, max-age=86400"

    return response


tutorials_discourse = Tutorials(
    parser=TutorialParser(
        api=DiscourseAPI(
            base_url="https://discourse.maas.io/",
            session=get_requests_session(),
            api_key=MAAS_DISCOURSE_API_KEY,
            api_username=MAAS_DISCOURSE_API_USERNAME,
            get_topics_query_id=2,
        ),
        index_topic_id=1289,
        url_prefix="/maas/tutorials",
    ),
    document_template="maas/_tutorial.html",
    url_prefix="/maas/tutorials",
    blueprint_name="maas-tutorials",
)


@app.route("/maas/tutorials")
def maas_tutorials():
    tutorials_discourse.parser.parse()
    tutorials_discourse.parser.parse_topic(
        tutorials_discourse.parser.index_topic
    )
    tutorials = tutorials_discourse.parser.tutorials
    topic_list = []

    for item in tutorials:
        if item["categories"] not in topic_list:
            topic_list.append(item["categories"])
        item["categories"] = {
            "slug": item["categories"],
            "name": " ".join(
                [word.capitalize() for word in item["categories"].split("-")]
            ),
        }

    topic_list.sort()
    topics = []

    for topic in topic_list:
        topics.append(
            {
                "slug": topic,
                "name": " ".join(
                    [word.capitalize() for word in topic.split("-")]
                ),
            }
        )

    return flask.render_template(
        "maas/tutorials.html",
        tutorials=tutorials,
        topics=topics,
    )


tutorials_discourse.init_app(app)


MAAS_BLOG_URL = "/maas/blog"
maas_blog_api = BlogAPI(
    session=search_session,
    thumbnail_width=354,
    thumbnail_height=199,
)
maas_blog = build_blueprint(
    BlogViews(
        api=maas_blog_api,
        blog_title="MAAS Blog",
        tag_ids=[1304],
        excluded_tags=[3184, 3265, 3408],
    ),
)

app.register_blueprint(maas_blog, url_prefix=MAAS_BLOG_URL, name="maas_blog")

app.add_url_rule(
    "/maas/blog/sitemap.xml",
    view_func=BlogSitemapIndex.as_view(
        "maas_blog_sitemap", blog_views=maas_blog
    ),
)

app.add_url_rule(
    "/maas/blog/sitemap/<regex('.+'):slug>.xml",
    view_func=BlogSitemapPage.as_view(
        "maas_blog_sitemap_page", blog_views=maas_blog
    ),
)


@app.before_request
def handle_maas_goget():
    """
    Handle go-get requests for /maas and /maas/* before normal routing.
    Return metadata for Go package manager
    That allows to do things like
    `go get canonical.com/maas/core/src/maasagent`
    by using Git repository at https://code.launchpad.net/maas
    """
    path = flask.request.path
    if (
        path == "/maas" or path.startswith("/maas/")
    ) and flask.request.query_string == b"go-get=1":
        return flask.render_template("maas/gomod.html"), 200


@app.errorhandler(502)
def bad_gateway(e):
    prefix = "502 Bad Gateway: "
    if str(e).find(prefix) != -1:
        message = str(e)[len(prefix) :]
    return flask.render_template("502.html", message=message), 502


@app.errorhandler(401)
def unauthorized_error(error):
    return (
        flask.render_template("401.html", message=error.description),
        500,
    )


def get_user_country_by_tz():
    """
    Get user country by timezone using ISO 3166 country codes.
    We store the country codes and timezones as static JSON files in the
    static/files directory.

    Eventually we plan to merge this function with the one below, once we
    are confident that takeovers won't be broken.
    """
    APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timezone = flask.request.args.get("tz")

    with open(
        os.path.join(APP_ROOT, "static/files/timezones.json"), "r"
    ) as file:
        timezones = json.load(file)

    with open(
        os.path.join(APP_ROOT, "static/files/countries.json"), "r"
    ) as file:
        countries = json.load(file)

    # Fallback to GB if timezone is invalid
    try:
        country_tz = timezones[timezone]
    except KeyError:
        country_tz = timezones["Europe/London"]

    # Check timezone of country alias if country code not found
    try:
        _country = country_tz["c"][0]
        country = countries[_country]
    except KeyError:
        try:
            alias = country_tz["a"]
            alias_tz = timezones[alias]
            _country = alias_tz["c"][0]
            country = countries[_country]
        except KeyError:
            country = "United Kingdom"
            _country = "GB"

    return flask.jsonify(
        {
            "country": country,
            "country_code": _country,
        }
    )


app.add_url_rule("/user-country-tz.json", view_func=get_user_country_by_tz)


app.add_url_rule(
    "/legal/contributors/agreement/api",
    methods=["POST", "GET"],
    view_func=canonical_cla_api_proxy,
)
app.add_url_rule(
    "/legal/contributors/agreement/api/github/logout",
    view_func=canonical_cla_api_github_logout,
)
app.add_url_rule(
    "/legal/contributors/agreement/api/github/login",
    view_func=canonical_cla_api_github_login,
)
app.add_url_rule(
    "/legal/contributors/agreement/api/launchpad/logout",
    view_func=canonical_cla_api_launchpad_logout,
)
app.add_url_rule(
    "/legal/contributors/agreement/api/launchpad/login",
    view_func=canonical_cla_api_launchpad_login,
)


@app.route("/multipass/download/<regex('windows|macos'):osname>")
def osredirect(osname):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_path = os.path.join(
        SITE_ROOT, "../static/files/latest-multipass-releases.json"
    )
    release = json.load(open(json_path))
    return flask.redirect(release["installer_urls"][osname], code=302)


@app.after_request
def no_cache(response):
    if flask.request.path == "/static/files/latest-multipass-release.json":
        response.cache_control.max_age = None
        response.cache_control.no_store = True
        response.cache_control.public = False

    return response


def build_case_study_index(engage_docs):
    def case_study_index():
        page = flask.request.args.get("page", default=1, type=int)
        preview = flask.request.args.get("preview")
        language = flask.request.args.get("language", default=None, type=str)
        tag = flask.request.args.get("tag", default=None, type=str)
        limit = 21
        offset = (page - 1) * limit

        if tag or language:
            (
                metadata,
                count,
                active_count,
                current_total,
            ) = engage_docs.get_index(
                limit,
                offset,
                tag_value=tag,
                key="type",
                value="case study",
                second_key="language",
                second_value=language,
            )
        else:
            (
                metadata,
                count,
                active_count,
                current_total,
            ) = engage_docs.get_index(
                limit, offset, key="type", value="case study"
            )
        total_pages = math.ceil(current_total / limit)

        for case_study in metadata:
            path = case_study["path"]
            if path.startswith("/engage"):
                case_study["path"] = "https://ubuntu.com" + path

        tags = engage_docs.get_engage_pages_tags()
        # strip whitespace, remove dupes and order alphabetically
        processed_tags = sorted({tag.strip() for tag in tags if tag.strip()})

        return flask.render_template(
            "case-study/index.html",
            forum_url=engage_docs.api.base_url,
            metadata=metadata,
            page=page,
            preview=preview,
            language=language,
            posts_per_page=limit,
            total_pages=total_pages,
            current_page=page,
            tags=processed_tags,
        )

    return case_study_index


# Case study
DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USERNAME = os.getenv("DISCOURSE_API_USERNAME")
engage_pages_discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=get_requests_session(),
    get_topics_query_id=14,
    api_key=DISCOURSE_API_KEY,
    api_username=DISCOURSE_API_USERNAME,
)
case_study_path = "/case-study"
case_studies = EngagePages(
    api=engage_pages_discourse_api,
    category_id=51,
    page_type="engage-pages",
    exclude_topics=[17229, 18033, 17250],
)

app.add_url_rule(
    case_study_path, view_func=build_case_study_index(case_studies)
)

# Mir Server
discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=search_session,
    api_key=DISCOURSE_API_KEY,
    api_username=DISCOURSE_API_USERNAME,
)


mir_url_prefix = "/mir/docs"
mir_docs = Docs(
    parser=DocParser(
        api=discourse_api,
        index_topic_id=27559,
        url_prefix=mir_url_prefix,
    ),
    blueprint_name="mir-server-docs",
    document_template="mir/docs/document.html",
    url_prefix=mir_url_prefix,
)

app.add_url_rule(
    "/mir/docs/search",
    "mir-docs-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/mir/docs",
        template_path="mir/docs/search-results.html",
    ),
)

mir_docs.init_app(app)


# Sitemap parser
def build_sitemap_tree(exclude_paths=None):
    def create_sitemap(sitemap_path):
        directory_path = os.getcwd() + "/templates"
        base_url = "https://canonical.com"
        try:
            xml_sitemap = directory_parser.generate_sitemap(
                directory_path, base_url, exclude_paths=exclude_paths
            )
            if xml_sitemap:
                with open(sitemap_path, "w") as f:
                    f.write(xml_sitemap)
                logging.info(f"Sitemap saved to {sitemap_path}")

                return xml_sitemap
            else:
                logging.warning("Sitemap is empty")
                return {"error:", "Sitemap is empty"}, 400

        except Exception as e:
            logging.error(f"Error generating sitemap: {e}")
            return f"Generate_sitemap error: {e}", 500

    def serve_sitemap():
        """
        Generate and serve the sitemap_tree.xml file.
        This sitemap tracks changes in the template files and is generated
        dynamically on every new push to main.
        """
        sitemap_path = os.getcwd() + "/templates/sitemap_tree.xml"

        # Update sitemap with POST request
        if flask.request.method == "POST":
            expected_secret = os.getenv("SITEMAP_SECRET")
            provided_secret = flask.request.headers.get(
                "Authorization", ""
            ).replace("Bearer ", "")

            if provided_secret != expected_secret:
                logging.warning("Invalid secret provided")
                return {"error": "Unauthorized"}, 401

            xml_sitemap = create_sitemap(sitemap_path)
            return {
                "message": (
                    f"Sitemap successfully generated at {sitemap_path}"
                )
            }, 200

        # Generate sitemap if it does not exist
        if not os.path.exists(sitemap_path):
            xml_sitemap = create_sitemap(sitemap_path)

        # Serve the existing sitemap
        with open(sitemap_path, "r") as f:
            xml_sitemap = f.read()

        response = flask.make_response(xml_sitemap)
        response.headers["Content-Type"] = "application/xml"
        return response

    return serve_sitemap


# Endpoint for retrieving parsed directory tree
def get_sitemaps_tree():
    try:
        tree = directory_parser.scan_directory(
            os.getcwd() + "/templates", exclude_paths=DYNAMIC_SITEMAPS
        )
    except Exception as e:
        return {"Error:": str(e)}, 500
    return tree


app.add_url_rule("/sitemap_parser", view_func=get_sitemaps_tree)
app.add_url_rule(
    "/sitemap_tree.xml",
    view_func=build_sitemap_tree(DYNAMIC_SITEMAPS),
    methods=["GET", "POST"],
)


@app.route("/solutions/infrastructure/private-cloud-pricing.json")
def get_pricing_data():
    """Serve pricing data with content-hash cache busting"""

    base_path = os.path.join(
        os.getcwd(), "static/json/private-cloud-pricing.json"
    )

    try:
        # Read file
        with open(base_path, "rb") as f:
            file_content = f.read()

        # Get hash
        content_hash = hashlib.md5(file_content).hexdigest()[:8]
        requested_version = flask.request.args.get("v")
        is_versioned_request = requested_version == content_hash

        # Check if client accepts gzip encoding
        accepts_gzip = "gzip" in flask.request.headers.get(
            "Accept-Encoding", ""
        )

        if accepts_gzip:
            data = gzip.compress(file_content)
            response = flask.make_response(data)
            response.headers["Content-Type"] = "application/json"
            response.headers["Content-Encoding"] = "gzip"
        else:
            response = flask.make_response(file_content)
            response.headers["Content-Type"] = "application/json"

        # Set cache headers based on versioning
        if is_versioned_request:
            response.headers["Cache-Control"] = (
                "public, max-age=31536000, immutable"
            )
        else:
            response.headers["Cache-Control"] = "public, max-age=300"

        response.headers["Vary"] = "Accept-Encoding"
        response.headers["X-Content-Hash"] = content_hash

        return response

    except FileNotFoundError:
        logger.error("Pricing data file not found")
        return {"error": "Pricing data not available"}, 500


# Custom redirects for Jaas
@app.route("/jaas/<charm_or_bundle_name>")
@app.route("/jaas/<charm_or_bundle_name>/<series_or_version>")
@app.route("/jaas/<charm_or_bundle_name>/<series_or_version>/<version>")
def details_redirect(
    charm_or_bundle_name,
    series_or_version=None,
    version=None,
):
    charmhub_url = "https://charmhub.io/" + charm_or_bundle_name
    return flask.redirect(charmhub_url, code=301)


# Create endpoints for testing environment only
if get_flask_env("DEBUG") or app.debug:

    @app.route("/tests/<path:subpath>")
    def tests(subpath):
        """
        Expose all routes under templates/tests if in development/testing mode.
        """
        print("subpath:", subpath)
        return flask.render_template(f"tests/{subpath}.html")
