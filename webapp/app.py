import flask
import datetime

from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder

from webapp.api import get_partner_groups


app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


def index():
    partner_groups = get_partner_groups()
    return flask.render_template("index.html", partner_groups=partner_groups)


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=index)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.context_processor
def inject_today_date():
    return {"current_year": datetime.date.today().year}
