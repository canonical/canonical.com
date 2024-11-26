# Standard library
import logging
import json
from functools import wraps
import datetime
import calendar
import os
import re
from urllib.parse import parse_qs, urlencode, urlparse

import bleach
import flask
import markdown

# Packages
from canonicalwebteam import image_template
from canonicalwebteam.blog import BlogAPI, BlogViews, build_blueprint
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam.discourse import DiscourseAPI, Docs, DocParser
from canonicalwebteam.search import build_search_view
from requests.exceptions import HTTPError
from slugify import slugify

# Local
from webapp.application import application
from webapp.greenhouse import Greenhouse, Harvest
from webapp.partners import Partners
from webapp.static_data import homepage_featured_products
from webapp.navigation import (
    get_current_page_bubble,
    build_navigation,
    split_list,
)
from webapp.requests_session import get_requests_session

logger = logging.getLogger(__name__)

CHARMHUB_DISCOURSE_API_KEY = os.getenv("CHARMHUB_DISCOURSE_API_KEY")
CHARMHUB_DISCOURSE_API_USERNAME = os.getenv("CHARMHUB_DISCOURSE_API_USERNAME")

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

charmhub_discourse_api = DiscourseAPI(
    base_url="https://discourse.charmhub.io/",
    session=get_requests_session(),
    api_key=CHARMHUB_DISCOURSE_API_KEY,
    api_username=CHARMHUB_DISCOURSE_API_USERNAME,
    get_topics_query_id=2,
)
search_session = get_requests_session()

app.register_blueprint(application, url_prefix="/careers/application")


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
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


@app.route("/sitemap-links.xml")
def home_sitemap():
    xml_sitemap = flask.render_template("sitemap-links.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    response.headers["Cache-Control"] = "public, max-age=43200"

    return response


app.add_url_rule(
    "/search",
    "search",
    build_search_view(
        app=app,
        session=search_session,
        template_path="search.html",
        search_engine_id=search_engine_id,
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
        return job_details(greenhouse, harvest, job_id)


def job_details(greenhouse, harvest, job_id):
    context = {"bleach": bleach}

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
    return flask.render_template("/careers/career-explorer.html")


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
    )


@app.route("/careers/hiring-process")
def hiring_process():
    return flask.render_template("careers/hiring-process/index.html")


# Company culture pages
@app.route("/careers/company-culture")
def culture():
    return flask.render_template("careers/company-culture/index.html")


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
        )
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
        [
            {"lat": 40.798155988207235, "lng": -73.85861239168297},
            "New York City",
        ],
        [{"lat": 25.019212561496353, "lng": 121.46383373680085}, "Taipei"],
        [{"lat": 30.355265001335628, "lng": -97.76687845245245}, "Austin"],
        [{"lat": 48.857074990278676, "lng": 2.3395547447652056}, "Paris"],
        [{"lat": 29.767193226058257, "lng": -95.3670538129764}, "Houston"],
        [{"lat": 35.8932740016975, "lng": 14.43746658277917}, "Malta"],
        [{"lat": 45.76429262112831, "lng": 4.835301390987176}, "Lyon"],
        [{"lat": 38.67917381627824, "lng": -90.20103074315858}, "St. Louis"],
        [{"lat": 49.345532689469906, "lng": -123.15343044637059}, "Vancouver"],
        [{"lat": 45.50646706624962, "lng": -73.54839431247403}, "Montreal"],
        [{"lat": 54.23314227514377, "lng": -4.491204453385781}, "Isle of Man"],
        [{"lat": 43.69252498079002, "lng": -79.35691360946339}, "Toronto"],
        [{"lat": 52.546559646531676, "lng": 13.479878094105333}, "Berlin"],
        [{"lat": 47.51053153079359, "lng": 19.092692050422652}, "Budapest"],
        [{"lat": 45.5599016546521, "lng": -122.57976576863925}, "Portland"],
        [{"lat": 39.9506480530072, "lng": -75.15098887376676}, "Philidelphia"],
        [{"lat": 37.63173475246442, "lng": 127.01153111181107}, "Seoul"],
        [{"lat": 50.93434695845433, "lng": 4.383602900267246}, "Brussels"],
        [{"lat": 49.25917985619196, "lng": 16.627178100791575}, "Brno"],
        [{"lat": -27.4687724806326, "lng": 153.02599001382598}, "Brisbane"],
        [{"lat": -33.865841276697054, "lng": 151.196327385238}, "Sydney"],
        [{"lat": 30.356430163416317, "lng": -97.71716022646561}, "Austin"],
        [{"lat": -33.45421283631078, "lng": -70.66577622308252}, "Santiago"],
        [{"lat": 39.748447785422016, "lng": -105.0168199879092}, "Denver"],
        [{"lat": 30.05563678743736, "lng": -89.82322663188988}, "New Orleans"],
        [{"lat": 52.24325667424824, "lng": 21.05145033879068}, "Warsaw"],
        [{"lat": 42.446882419194324, "lng": -71.22491732631751}, "Lexington"],
        [{"lat": 34.35676353830776, "lng": -111.51505767860898}, "Arizona"],
        [{"lat": 25.763155578558653, "lng": 54.94246340504953}, "Dubai"],
        [{"lat": 47.65006756574396, "lng": -122.35867431899362}, "Seattle"],
        [{"lat": 37.42579354504801, "lng": -78.17007396261319}, "Virginia"],
        [{"lat": 39.70820784971259, "lng": -8.484528745678654}, "Portugal"],
        [{"lat": 14.567870738893827, "lng": 120.93577783953602}, "Manilla"],
        [{"lat": 39.382464124962944, "lng": -105.64887008422835}, "Colorado"],
        [
            {"lat": 40.77912659323516, "lng": -112.04853012171523},
            "Salt Lake City",
        ],
        [
            {"lat": 52.57604547428001, "lng": -0.1826908772221332},
            "Peterborough",
        ],
        [{"lat": 37.9823636439218, "lng": 23.7456050381961}, "Athens"],
        [{"lat": 49.47243608230826, "lng": 11.19116713398345}, "Nuremberg"],
        [{"lat": 44.47558032183258, "lng": 26.094270552088407}, "Bucharest"],
        [{"lat": 51.051617091670444, "lng": 3.732070061271262}, "Ghent"],
        [{"lat": 25.761635180712478, "lng": -80.20101769294185}, "Miami"],
        [{"lat": 45.901473355934364, "lng": 6.13502570130426}, "Annecy"],
        [{"lat": 51.234949685621814, "lng": 3.2142528855251635}, "Bruges"],
        [{"lat": 28.535137392578626, "lng": -81.4092377509802}, "Orlando"],
    ]

    return flask.render_template(
        f"{flask.request.path}.html",
        sprint_locations=sprint_locations,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
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
@app.route("/partners/devices-and-iot")
def handle_partner_details():
    with get_requests_session() as session:
        partners_api = Partners(session)
        return partner_details(partners_api)


def partner_details(partners_api):
    partners = partners_api._get(
        partners_api.partner_page_map[flask.request.path.split("/")[2]]
    )
    return flask.render_template(
        f"{flask.request.path}.html", partners=partners
    )


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


@app.context_processor
def utility_processor():
    return {"image": image_template}


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

# Data Platform PostgreSQL on K8s docs
data_postgresql_k8s_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=9307,
        url_prefix="/data/docs/postgresql/k8s",
    ),
    document_template="/data/docs/postgresql/k8s/document.html",
    url_prefix="/data/docs/postgresql/k8s",
    blueprint_name="data-docs-postgresql-k8s",
)
app.add_url_rule(
    "/data/docs/postgresql/k8s/search",
    "data-docs-postgresql-k8s-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/postgresql/k8s",
        template_path="/data/docs/postgresql/k8s/search-results.html",
    ),
)
data_postgresql_k8s_docs.init_app(app)

# Data Platform PostgreSQL on IaaS docs
data_postgresql_iaas_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=9710,
        url_prefix="/data/docs/postgresql/iaas",
    ),
    document_template="/data/docs/postgresql/iaas/document.html",
    url_prefix="/data/docs/postgresql/iaas",
    blueprint_name="data-docs-postgresql-iaas",
)
app.add_url_rule(
    "/data/docs/postgresql/iaas/search",
    "data-docs-postgresql-iaas-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/postgresql/iaas",
        template_path="/data/docs/postgresql/iaas/search-results.html",
    ),
)
data_postgresql_iaas_docs.init_app(app)

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

# Data Platform Kafka on IaaS docs
data_kafka_iaas_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=10288,
        url_prefix="/data/docs/kafka/iaas",
    ),
    document_template="/data/docs/kafka/iaas/document.html",
    url_prefix="/data/docs/kafka/iaas",
    blueprint_name="data-docs-kafka-iaas",
)
app.add_url_rule(
    "/data/docs/kafka/iaas/search",
    "data-docs-kafka-iaas-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/kafka/iaas",
        template_path="/data/docs/kafka/iaas/search-results.html",
    ),
)
data_kafka_iaas_docs.init_app(app)

# Data Platform Kafka on K8s docs
data_kafka_k8s_docs = Docs(
    parser=DocParser(
        api=charmhub_discourse_api,
        index_topic_id=10296,
        url_prefix="/data/docs/kafka/k8s",
    ),
    document_template="/data/docs/kafka/k8s/document.html",
    url_prefix="/data/docs/kafka/k8s",
    blueprint_name="data-docs-kafka-k8s",
)
app.add_url_rule(
    "/data/docs/kafka/k8s/search",
    "data-docs-kafka-k8s-search",
    build_search_view(
        app=app,
        session=search_session,
        site="canonical.com/data/docs/kafka/k8s",
        template_path="/data/docs/kafka/k8s/search-results.html",
    ),
)
data_kafka_k8s_docs.init_app(app)

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

# Mirostack docs
microstack_docs = Docs(
    parser=DocParser(
        api=DiscourseAPI(
            base_url="https://discourse.ubuntu.com/",
            session=get_requests_session(),
        ),
        index_topic_id=18212,
        url_prefix="/microstack/docs",
    ),
    document_template="/microstack/docs/document.html",
    url_prefix="/microstack/docs",
    blueprint_name="microstack_docs",
)

microstack_docs.init_app(app)


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


def render_form(form):
    @wraps(render_form)
    def wrapper_func():
        with app.app_context() and app.test_request_context():
            return flask.render_template(
                form["templatePath"],
                fieldsets=form["fieldsets"],
                formData=form["formData"],
                isModal=form.get("isModal"),
                modalId=form.get("modalId"),
            )

    return wrapper_func


def set_form_rules():
    filename = os.path.join(app.static_folder, "files", "forms-data.json")
    with open(filename) as forms:
        data = json.load(forms)
        for path, form in data["forms"].items():
            app.add_url_rule(path, view_func=render_form(form), endpoint=path)


# this causes secondary navigation to dissapear
# on /data/opensearch and /data/postresql
# see: https://github.com/canonical/canonical.com/issues/1399
# set_form_rules()
