# Standard library
import datetime
import flask
import markdown
import os
import re

# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from slugify import slugify
import talisker.requests

# Local
from webapp.greenhouse import Greenhouse
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
greenhouse_api = Greenhouse(session)
greenhouse_api_key = os.environ.get("GREENHOUSE_API_KEY")
partners_api = Partners(session)


@app.route("/")
def index():
    partner_groups = partners_api.get_partner_groups()
    return flask.render_template("index.html", partner_groups=partner_groups)


@app.route("/secure-boot-master-ca.crl")
def secure_boot():
    return flask.send_from_directory(
        "../static/files", "secure-boot-master-ca.crl"
    )


# Career departments
@app.route("/careers/results")
def results():
    context = {}
    vacancies = []
    departments = []
    message = ""
    if flask.request.args:
        core_skills = flask.request.args["coreSkills"].split(",")
        context["core_skills"] = core_skills
        vacancies = greenhouse_api.get_vacancies_by_skills(core_skills)
    else:
        message = "There are no roles matching your selection."
    if len(vacancies) == 0:
        message = "There are no roles matching your selection."
    else:
        for job in vacancies:
            if not (job["department"] in departments):
                departments.append(job["department"])
    context["message"] = message
    context["vacancies"] = vacancies
    context["departments"] = departments

    return flask.render_template("careers/results.html", **context)

"""
@app.route("/careers/admin", methods=["GET", "POST"])
@app.route("/careers/all", methods=["GET", "POST"])
@app.route("/careers/commercial-ops", methods=["GET", "POST"])
@app.route("/careers/design", methods=["GET", "POST"])
@app.route("/careers/engineering", methods=["GET", "POST"])
@app.route("/careers/finance", methods=["GET", "POST"])
@app.route("/careers/hr", methods=["GET", "POST"])
@app.route("/careers/legal", methods=["GET", "POST"])
@app.route("/careers/marketing", methods=["GET", "POST"])
@app.route("/careers/project-management", methods=["GET", "POST"])
@app.route("/careers/sales", methods=["GET", "POST"])
@app.route("/careers/tech-ops", methods=["GET", "POST"])
def department_group():
    department = flask.request.path.split("/")[2]
    vacancies = greenhouse_api.get_vacancies(department)
    all_departments = greenhouse_api.get_all_departments()
    department_slugs = greenhouse_api.get_vacancy_department_slugs()
    department_navigation = []

    #careers_directory = os.listdir(os.path.join(app.template_folder, "careers"))
    careers_directory = os.listdir("./templates/careers")

    for slug in department_slugs:
        if not (slug in department_navigation):
            department_navigation.append(slug)

    for template in careers_directory:
        if template.endswith(".html"):
            for name in all_departments:
                department_slug = name.lower().replace(" ", ",")
                template_slug = os.fsdecode(template)
                template_slug = template_slug[:-5]
                if department_slug == template_slug:
                    if not (department_slug in department_navigation):
                        department_navigation.append(department_slug)


    if flask.request.method == "POST":
        response = greenhouse_api.submit_application(
            os.environ["GREENHOUSE_API_KEY"],
            flask.request.form,
            flask.request.files,
        )
        if response.status_code == 200:
            message = {
                "type": "positive",
                "title": "Success",
                "text": (
                    "Your application has been successfully submitted."
                    " Thank you!"
                ),
            }
        else:
            message = {
                "type": "negative",
                "title": f"Error {response.status_code}",
                "text": f"{response.reason}. Please try again!",
            }

        return flask.render_template(
            f"careers/{department}.html", vacancies=vacancies, message=message
        )

    return flask.render_template(
        f"careers/{department}.html", vacancies=vacancies, department_navigation=department_navigation
    )
"""

class Department(object):
    __careers_directory = "./templates/careers"
    def __parse_feed_department(feed_department):
        field = {
            "cloud engineering": "engineering",
            "device engineering": "engineering",
            "web and design": "design",
            "operations": "commercialops",
            "human resources": "hr",
        }

        if feed_department.lower() in field:
            return field[feed_department.lower()]

        return feed_department

    def get_template_name(self):
        careers_directory = os.listdir(Department.__careers_directory)
        for template in careers_directory:
            if template.endswith(".html"):
                if template[:-5].replace("-", "") == Department.__parse_feed_department(self.name.replace("-", "")):
                    return template[:-5]
        return None
    
    def get_title(self):
        if self.template_slug:
            path = Department.__careers_directory + "/" + self.template_slug + ".html"
            if os.path.exists(path):
                with open(path) as reader:
                    for line in reader:
                        if line.startswith("{% block title %}"):
                            return line[line.index("}") + 1 : line.rindex("{")]
        
        return self.name.title()


    def __init__(self, name):
        self.name = name
        self.slug = Department.__parse_feed_department(name).lower().replace(" ", "-")
        self.template_slug = self.get_template_name()
        self.title = self.get_title()

def generate_department_pages():
    departments = []
    vacancies = greenhouse_api.get_vacancies("all")
    all_departments = greenhouse_api.get_all_departments()
    careers_directory = os.listdir("./templates/careers")

    departments.append(Department("admin"))
    departments.append(Department("all"))
    
    # Get departments from vacancy list
    for vacancy in vacancies:
        new_dept = Department(vacancy["department"])
        is_new = True
        for department in departments:
            if department.title == new_dept.title:
                is_new = False
                break
        if is_new:
            departments.append(new_dept)
    
    # Get departments from department list that have templates
    for template in careers_directory:
        if template.endswith(".html"):
            for name in all_departments:
                department_slug = name.lower().replace(" ", ",")
                template_slug = os.fsdecode(template)
                template_slug = template_slug[:-5]
                if department_slug == template_slug:
                    new_dept = Department(name)
                    for department in departments:
                        if department.title == new_dept.title:
                            is_new = False
                            break
                    if is_new:
                        departments.append(new_dept)
    
    # Make a page for each department
    for department in departments:
        path ="/careers/"
        if department.template_slug:
            slug = template_slug
        else:
            slug = department_slug
        path += slug
        # Does not work - each app.route needs to have a unique function name. Try rewriting this with dynamic path names.
        @app.route(path, methods=["GET", "POST"])
        def department_group():
            vacancies = greenhouse_api.get_vacancies(slug)

            if flask.request.method == "POST":
                response = greenhouse_api.submit_application(
                    os.environ["GREENHOUSE_API_KEY"],
                    flask.request.form,
                    flask.request.files,
                )
                if response.status_code == 200:
                    message = {
                        "type": "positive",
                        "title": "Success",
                        "text": (
                            "Your application has been successfully submitted."
                            " Thank you!"
                        ),
                    }
                else:
                    message = {
                        "type": "negative",
                        "title": f"Error {response.status_code}",
                        "text": f"{response.reason}. Please try again!",
                    }

                return flask.render_template(
                    f"careers/{department}.html", vacancies=vacancies, message=message, departments=departments
                )

            return flask.render_template(
                f"careers/{department}.html", vacancies=vacancies, department=deaprtments
            )

generate_department_pages()


@app.route("/careers/<regex('[0-9]+'):job_id>", methods=["GET", "POST"])
def job_details(job_id):
    job = greenhouse_api.get_vacancy(job_id)
    if not job:
        flask.abort(404)

    if flask.request.method == "POST":
        response = greenhouse_api.submit_application(
            greenhouse_api_key, flask.request.form, flask.request.files, job_id
        )
        if response.status_code == 200:
            message = {
                "type": "positive",
                "title": "Success",
                "text": (
                    "Your application has been successfully submitted."
                    " Thank you!"
                ),
            }
        else:
            message = {
                "type": "negative",
                "title": f"Error {response.status_code}",
                "text": f"{response.reason}. Please try again!",
            }

        return flask.render_template(
            f"/careers/job-detail.html", job=job, message=message
        )

    return flask.render_template("/careers/job-detail.html", job=job)


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
def partner_details():
    partners = partners_api._get(
        partners_api.partner_page_map[flask.request.path.split("/")[2]]
    )
    return flask.render_template(
        f"{flask.request.path}.html", partners=partners
    )


# Template finder
template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.context_processor
def inject_today_date():
    return {"current_year": datetime.date.today().year}


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
