import os
import socket
from dateutil.parser import parse

import flask
import talisker.requests

from webapp.greenhouse import Harvest
from webapp.utils.cipher import Cipher

application = flask.Blueprint(
    "application",
    __name__,
    template_folder="/templates",
    static_folder="/dist",
)

session = talisker.requests.get_session()
harvest = Harvest(session=session, api_key=os.environ.get("HARVEST_API_KEY"))
cipher = Cipher(os.environ.get("APPLICATION_CRYPTO_SECRET_KEY"))


@application.after_request
def add_headers(response):
    """
    Generic rules for headers to add to all requests

    - X-Hostname: Mention the name of the host/pod running the application
    - Cache-Control: Add cache-control headers for public and private pages
    """

    response.headers["X-Hostname"] = socket.gethostname()

    if response.status_code == 200:
        response.headers["Cache-Control"] = "private"

    return response


def stage_progress(current_stage):
    # TODO FINISH THIS CODE (currently just for demo)
    if current_stage == "Application Review":
        return {
            "application": True,
            "assessment": False,
            "early_stage": False,
            "late_stage": False,
            "offer": False,
        }
    if current_stage == "Written Interview":
        return {
            "application": True,
            "assessment": True,
            "early_stage": False,
            "late_stage": False,
            "offer": False,
        }

    return {
        "application": True,
        "assessment": True,
        "early_stage": True,
        "late_stage": False,
        "offer": False,
    }


@application.route("/<string:token>")
def application_page(token):
    decrypted = cipher.decrypt(token)
    if not decrypted:
        flask.abort(404)
    name, candidate_id, application_id = tuple(decrypted.split("-"))
    candidate_id, application_id = int(candidate_id), int(application_id)
    application = harvest.get_application(application_id)
    if (
        "candidate_id" not in application
        or application["candidate_id"] != candidate_id
    ):
        flask.abort(404)

    candidate = harvest.get_candidate(application["candidate_id"])
    if not candidate["first_name"].lower() == name:
        flask.abort(404)

    if application["current_stage"]:
        application["stage_progress"] = stage_progress(
            application["current_stage"]["name"]
        )
        application["scheduled_interviews"] = harvest.get_interviews_scheduled(
            application_id
        )

        for interview in application["scheduled_interviews"]:
            interview["start"]["datetime"] = parse(
                interview["start"]["date_time"]
            )
            interview["end"]["datetime"] = parse(interview["end"]["date_time"])
            difference = (
                interview["end"]["datetime"] - interview["start"]["datetime"]
            )
            interview["duration"] = int(difference.total_seconds() / 60)

    job = harvest.get_job(application["jobs"][0]["id"])

    hiring_lead = None
    for recruiter in job["hiring_team"]["recruiters"]:
        if recruiter["responsible"]:
            hiring_lead = harvest.get_user(recruiter["id"])
            break

    return flask.render_template(
        "applications/application.html",
        title="You application",
        candidate=candidate,
        application=application,
        job=job,
        hiring_lead=hiring_lead,
    )