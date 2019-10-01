# Standard library
import datetime
import flask
import markdown
import re


# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from slugify import slugify


# Local
from webapp.greenhouse_api import (
    get_vacancies,
    get_vacancy,
    remove_hyphens,
    submit_to_greenhouse,
)
from webapp.partners_api import get_partner_groups, get_partner_list

app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


@app.route("/")
def index():
    partner_groups = get_partner_groups()
    return flask.render_template("index.html", partner_groups=partner_groups)


# Career departments
@app.route("/careers/results")
def results():
    context = {}
    vacancies = []
    message = ""
    if flask.request.args:
        departments = flask.request.args["departments"].split(",")
        context["departments"] = departments
        for department in departments:
            vacancies = vacancies + get_vacancies(department)
    else:
        message = "There are no roles matching your selection."
    context["message"] = message
    context["vacancies"] = vacancies

    return flask.render_template("careers/results.html", **context)


@app.route("/careers/<department>", methods=["GET", "POST"])
def department_group(department):
    vacancies = get_vacancies(department)

    if flask.request.method == "POST":
        response = submit_to_greenhouse(
            flask.request.form, flask.request.files
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
        f"careers/{department}.html", vacancies=vacancies
    )


@app.route("/careers/<department>/<job_id>")
def job_details(department, job_id):
    job = get_vacancy(job_id)
    if (
        remove_hyphens(job["department"]).lower()
        != remove_hyphens(department).lower()
        and "all" != department.lower()
    ):
        flask.abort(404)

    return flask.render_template("/careers/jobs/job-detail.html", job=job)


@app.route("/careers/<department>/<job_id>", methods=["POST"])
def submit_job(department, job_id):
    print("It works")
    return flask.render_template("/careers/jobs/index.html")


# Partners
@app.route("/partners/find-a-partner")
def find_a_partner():
    partners = sorted(get_partner_list(), key=lambda item: item["name"])
    return flask.render_template(
        "/partners/find-a-partner.html", partners=partners
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
    short_path = path.split("/")[1]

    return short_path


@app.template_filter()
def slug(text):
    return slugify(text)


@app.template_filter()
def markup(text):
    return markdown.markdown(text)
