import os
import flask
from canonicalwebteam.flask_base.app import FlaskBase

from canonicalwebteam.templatefinder import TemplateFinder

dir_path = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(dir_path)
templates_dir = os.path.join(app_dir, "templates")

app = FlaskBase(
    __name__,
    "canonical.com",
    template_folder=templates_dir,
    static_folder="../static",
)

template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.errorhandler(404)
def not_found_error(error):
    return flask.render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return flask.render_template("500.html"), 500
