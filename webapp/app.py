# Standard library
import os

# Packages
import flask
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder


dir_path = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(dir_path)
templates_dir = os.path.join(app_dir, "templates")

app = FlaskBase(
    __name__,
    "canonical.com",
    favicon_url="https://assets.ubuntu.com/v1/49a1a858-favicon-32x32.png",
    template_404="404.html",
    template_500="500.html",
    template_folder=templates_dir,
    static_folder="../static",
)

template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)


@app.route("/error")
def error_route():
    flask.abort(500)
