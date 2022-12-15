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


@app.route("/")
def index():
    return flask.render_template("index.html")


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

    return vacancies_by_department


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
        # Temporary fix to exlude a spammy domain
        # https://github.com/canonical-web-and-design/canonical.com/issues/437
        if flask.request.form["email"].endswith("qq.com"):
            flask.abort(406)

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


@app.route("/careers/start")
def start_career():
    return flask.render_template("/careers/career-explorer.html")


@app.route("/careers")
def careers_index():
    """
    Create a dictionary containing number of roles, slug
    and department name for a given department
    """

    all_departments = (_group_by_department(greenhouse.get_vacancies()),)

    dept_list = [
        "engineering",
        "techops",
        "marketing",
        "web-and-design",
        "project-management",
        "operations",
        "product",
        "sales",
        "finance",
        "human-resources",
    ]

    departments_overview = []

    for vacancy in all_departments:
        for dept in dept_list:
            if vacancy[dept]:
                count = len(vacancy[dept].__dict__["vacancies"])

                if dept == "techops":
                    name = "Support Engineering"
                    slug = "support-engineering"
                elif dept == "human-resources":
                    name = "People"
                    slug = "people"
                else:
                    name = vacancy[dept].__dict__["name"]
                    slug = vacancy[dept].__dict__["slug"]

                departments_overview.append(
                    {
                        "name": name,
                        "count": count,
                        "slug": slug,
                    }
                )

    return flask.render_template(
        "/careers/index.html",
        all_departments=all_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
        departments_overview=departments_overview,
    )


def get_sorted_departments():
    all_departments = (_group_by_department(greenhouse.get_vacancies()),)

    dept_order = [
        "engineering",
        "support-engineering",
        "marketing",
        "web-and-design",
        "project-management",
        "operations",
        "product",
        "sales",
        "finance",
        "people",
    ]

    dept_list = all_departments[0]

    # rename hr department and slug
    if "human-resources" in dept_list:
        dept_list["people"] = dept_list["human-resources"]
        del dept_list["human-resources"]
        dept_value = dept_list["people"].__dict__
        dept_value["name"] = "People"
        dept_value["slug"] = "people"

    if "techops" in dept_list:
        dept_list["support-engineering"] = dept_list["techops"]
        del dept_list["techops"]
        dept_value = dept_list["support-engineering"].__dict__
        dept_value["name"] = "Support Engineering"
        dept_value["slug"] = "support-engineering"

    return {k: dept_list[k] for k in dept_order}


@app.route("/careers/all")
def all_careers():

    sorted_departments = get_sorted_departments()

    return flask.render_template(
        "/careers/all.html",
        sorted_departments=sorted_departments,
        vacancies=[
            vacancy.to_dict() for vacancy in greenhouse.get_vacancies()
        ],
    )


@app.route("/careers/<department_slug>", methods=["GET", "POST"])
def department_group(department_slug):
    context = {
        "all_departments": _group_by_department(greenhouse.get_vacancies())
    }
    context["department"] = None
    templates = []

    # Generate list of templates in the /templates/careers folder,
    # and remove the .html suffix
    for template in os.listdir("./templates/careers"):
        if template.endswith(".html"):
            template = template[:-5]
        templates.append(template)

    # Check if deparment exist or return 404
    for slug, department in context["all_departments"].items():
        if department.slug == department_slug:
            context["department"] = department
            context["vacancies"] = greenhouse.get_vacancies_by_department_slug(
                department.slug
            )

    if not context["department"] and department_slug not in templates:
        flask.abort(404)

    vacancies = (
        [vacancy.to_dict() for vacancy in greenhouse.get_vacancies()],
    )

    featured_jobs = []
    fast_track_jobs = []

    for vacancy in vacancies[0]:
        # Check for department name discrepancies
        if vacancy["departments"] == "Human Resources":
            vacancy["departments"] = "People"

        if vacancy["departments"] == "Web & Design":
            vacancy["departments"] = "Web-and-Design"

        if vacancy["departments"] == "TechOps":
            vacancy["departments"] = "Support-Engineering"

        # Check if department role is featured or fast track
        if (
            vacancy["featured"]
            and vacancy["departments"].lower() == department_slug
        ):
            featured_jobs.append(vacancy)

        if (
            vacancy["fast_track"]
            and vacancy["departments"].lower() == department_slug
        ):
            fast_track_jobs.append(vacancy)

    context["templates"] = templates
    sorted_departments = get_sorted_departments()

    if flask.request.method == "POST":
        response = greenhouse.submit_application(
            flask.request.form,
            flask.request.files,
        )
        if response.status_code == 200:
            return flask.render_template("/careers/thank-you.html", **context)

        else:
            message = {
                "type": "negative",
                "title": f"Error {response.status_code}",
                "text": f"{response.reason}. Please try again!",
            }

        context["message"] = message

        return flask.render_template(
            "careers/base-template.html",
            sorted_departments=sorted_departments,
            **context,
        )

    return flask.render_template(
        "careers/base-template.html",
        sorted_departments=sorted_departments,
        featured_jobs=featured_jobs,
        fast_track_jobs=fast_track_jobs,
        department_slug=department_slug,
        **context,
    )


# Partners
@app.route("/partners/find-a-partner")
def find_a_partner():
    partners = sorted(
        partners_api.get_partner_list(), key=lambda item: item["name"]
    )
    return flask.render_template(
        "/partners/find-a-partner.html", partners=partners
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
    return flask.render_template("/502.html", message=message), 502
