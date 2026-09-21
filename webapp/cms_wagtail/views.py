import flask
import requests

from webapp.cms_wagtail.client import WagtailContent

TEMPLATES = {"website.CaseStudyPage": "cms_wagtail/case_study.html"}
DEFAULT_TEMPLATE = "cms_wagtail/page.html"
# Must match the url_prefix build_cms_wagtail_blueprint() is registered
# with in webapp/app.py, so log lines read as blueprint-relative paths
# rather than the app's full mount point.
BLUEPRINT_PREFIX = "/cms-wagtail"


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
        # Log the exception type and the incoming request's own path,
        # never the exception itself: requests' raise_for_status() puts
        # the full upstream URL - including a preview's ?token=... - in
        # its message, and str(error) would put a live preview
        # credential in the logs on every non-404 CMS error.
        # request.path excludes the query string by construction, so it
        # cannot carry that token even for this same preview request.
        path = flask.request.path
        if path.startswith(BLUEPRINT_PREFIX):
            path = path[len(BLUEPRINT_PREFIX) :] or "/"
        flask.current_app.logger.warning(
            "Wagtail CMS unavailable: %s for %s",
            type(error).__name__,
            path,
        )
        # Return, do not abort(): an exception raised inside an error
        # handler is not handled again and would surface as a 500.
        return flask.Response("The CMS is unavailable.", status=502)

    @blueprint.route("/_preview")
    def preview():
        content_type = flask.request.args.get("content_type")
        token = flask.request.args.get("token")
        if not (content_type and token):
            flask.abort(400)
        document = content().preview(content_type, token) or flask.abort(404)
        template = TEMPLATES.get(document["type"], DEFAULT_TEMPLATE)
        response = flask.make_response(
            flask.render_template(template, page=document, preview=True)
        )
        response.cache_control.no_store = True
        response.headers["X-Robots-Tag"] = "noindex"
        return response

    @blueprint.route("/<path:path>")
    def page(path):
        document = content().page_by_path(path) or flask.abort(404)
        template = TEMPLATES.get(document["type"], DEFAULT_TEMPLATE)
        return render(template, page=document, preview=False)

    return blueprint
