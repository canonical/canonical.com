# Standard library
import flask
import datetime
import re


# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder


# Local
from webapp.api import get_partner_groups
from webapp.get_job_feed import get_vacancies, get_vacancy

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
@app.route("/careers/<department>")
def department_group(department):
    vacancies = get_vacancies(department)

    return flask.render_template(
        f"careers/{department}.html", vacancies=vacancies
    )


@app.route("/careers/<department>/<job_id>")
def job_details(department, job_id):
    job = get_vacancy(job_id)

    if (
        remove_special_chars(job["department"])
        != remove_special_chars(department)
        and "all" != department
    ):
        flask.abort(404)

    return flask.render_template("/careers/jobs/job-detail.html", job=job)


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


def remove_special_chars(text):
    new_text = re.sub("[^A-Za-z0-9]+", "", text.lower())
    return new_text
