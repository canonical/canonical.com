import flask
import requests

from webapp.cms_wagtail.client import WagtailContent


def build_cms_wagtail_blueprint(session):
    blueprint = flask.Blueprint("cms_wagtail", __name__)

    def content():
        config = flask.current_app.config
        return WagtailContent(
            session,
            config["CMS_WAGTAIL_API_URL"],
            site_host=config["CMS_WAGTAIL_SITE_HOST"],
        )

    def render(template, **context):
        response = flask.make_response(
            flask.render_template(template, **context)
        )
        # PoC: always revalidate so published edits show immediately.
        response.cache_control.no_cache = True
        return response

    @blueprint.errorhandler(requests.RequestException)
    def cms_unavailable(error):
        flask.current_app.logger.warning("Wagtail CMS unavailable: %s", error)
        # Return, do not abort(): an exception raised inside an error
        # handler is not handled again and would surface as a 500.
        return flask.Response("The CMS is unavailable.", status=502)

    @blueprint.route("/<path:path>")
    def page(path):
        document = content().page_by_path(path) or flask.abort(404)
        return render("cms_wagtail/page.html", page=document, preview=False)

    return blueprint
