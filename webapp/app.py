# Standard library
import datetime
import calendar
import os
import re
from urllib.parse import parse_qs, urlencode, urlparse

import bleach
import flask
import markdown
import talisker.requests

# Packages
from canonicalwebteam import image_template
from canonicalwebteam.blog import BlogAPI, BlogViews, build_blueprint
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from requests.exceptions import HTTPError
from slugify import slugify

# Local
from webapp.application import application
from webapp.greenhouse import Greenhouse, Harvest
from webapp.partners import Partners
from webapp.static_data import homepage_featured_products

app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)
session = talisker.requests.get_session()
greenhouse = Greenhouse(
    session=session, api_key=os.environ.get("GREENHOUSE_API_KEY")
)
harvest = Harvest(session=session, api_key=os.environ.get("HARVEST_API_KEY"))
partners_api = Partners(session)

app.register_blueprint(application, url_prefix="/careers/application")


def _group_by_department(vacancies):
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


def _get_sorted_departments():
    departments = _group_by_department(greenhouse.get_vacancies())

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


def _get_all_departments() -> tuple:
    """
    Refactor for careers search section
    """
    all_departments = (_group_by_department(greenhouse.get_vacancies()),)

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


@app.route("/secure-boot-master-ca.crl")
def secure_boot():
    return flask.send_from_directory(
        "../static/files", "secure-boot-master-ca.crl"
    )


# Career departments
@app.route("/careers/diversity")
def diversity():
    context = {
        "all_departments": _group_by_department(greenhouse.get_vacancies())
    }
    context["department"] = None
    return flask.render_template("careers/diversity/index.html", **context)


@app.route("/careers/diversity/identity")
def identity():
    context = {
        "all_departments": _group_by_department(greenhouse.get_vacancies())
    }
    context["department"] = None
    return flask.render_template("careers/diversity/identity.html", **context)


@app.route("/careers/results")
def results():
    vacancies = []

    core_skills = flask.request.args.get("core-skills", "").split(",")
    vacancies = greenhouse.get_vacancies_by_skills(core_skills)
    vacancies_by_department = _group_by_department(vacancies)

    context = {
        "all_departments": _group_by_department(greenhouse.get_vacancies()),
        "vacancies": vacancies,
        "vacancies_by_department": vacancies_by_department,
    }

    return flask.render_template("careers/results.html", **context)


@app.route("/careers/company-culture")
def culture():
    return flask.render_template("careers/company-culture.html")


@app.route("/careers/sitemap.xml")
def careers_sitemap():
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
def careers_rss():
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
def job_details(job_id, job_title):
    context = {"bleach": bleach}

    try:
        context["job"] = greenhouse.get_vacancy(job_id)
    except HTTPError as error:
        if error.response.status_code == 404:
            flask.abort(404)
        else:
            raise error

    if not context["job"]:
        flask.abort(404)

    if flask.request.method == "POST":
        response = greenhouse.submit_application(
            flask.request.form, flask.request.files, job_id
        )
        if response.status_code == 200:
            return flask.render_template("/careers/thank-you.html", **context)

        else:
            context["message"] = {
                "type": "negative",
                "title": f"Error {response.status_code}",
                "text": f"{response.reason}. Please try again!",
            }

        return flask.render_template("/careers/job-detail.html", **context)

    return flask.render_template("/careers/job-detail.html", **context)


@app.route("/careers/career-explorer")
def start_career():
    return flask.render_template("/careers/career-explorer.html")


@app.route("/careers")
def careers_index():
    """
    Create a dictionary containing number of roles, slug
    and department name for a given department
    """

    all_departments, departments_overview = _get_all_departments()

    return flask.render_template(
        "/careers/index.html",
        all_departments=all_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        departments_overview=departments_overview,
    )


@app.route("/careers/progression")
def careers_progression():
    all_departments, departments_overview = _get_all_departments()

    return flask.render_template(
        "/careers/progression.html",
        all_departments=all_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        departments_overview=departments_overview,
    )


@app.route("/careers/all")
def all_careers():
    sorted_departments = _get_sorted_departments()

    return flask.render_template(
        "/careers/all.html",
        sorted_departments=sorted_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
    )


@app.route("/careers/company-culture/remote-work")
@app.route("/careers/company-culture/sustainability")
def working_here_pages():
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
def department_group(department_slug):
    departments = _get_sorted_departments()

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
        "careers/base-template.html",
        department=department,
        sorted_departments=departments,
        featured_jobs=featured_jobs,
        fast_track_jobs=fast_track_jobs,
        formatted_slug=formatted_slug,
        templates=templates,
    )


# Partners
@app.route("/partners/find-a-partner")
def find_a_partner():
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
@app.route("/partners/devices-and-iot")
def partner_details():
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


blog_views = BlogViews(
    api=BlogAPI(session=session),
    excluded_tags=[3184, 3265],
    per_page=11,
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
