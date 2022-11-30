import json
import os
import socket
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parseaddr
from smtplib import SMTP

import flask
import talisker.requests
from dateutil.parser import parse

from webapp.greenhouse import Harvest
from webapp.job_regions import regions
from webapp.utils.cipher import Cipher

withdrawal_reasons = {
    "27987": "I've accepted another position",
    "27992": "I've decided to stay with my current employer",
    "35818": "The position isn't a good fit",
    "36714": "I cannot complete the assessment",
    "33": "Other",
}

milestone_stages = {
    "application": {("Application Review")},
    "assessment": (
        "Written Interview",
        "Thomas International - GIA",
        "Psychometric Assessment",
        "Meet & Greet",
        "Peer Interview",
        "Phone Interview",
        "Domain Expert Screen",
    ),
    "early_stage": (
        "Early Stage Interviews",
        "Thomas International - PPA",
        "ClassMarker",
        "Devskiller",
        "Take Home Test",
        "Technical Exercise",
        "Exec Interview",
        "Reference Check",
        "HR Interview",
        "Technical Interview",
        "Technical Assessment Classmarker",
        "Talent Interview",
    ),
    "late_stage": (
        "Late Stage Interviews",
        "Executive Review",
        "Python Interview - Advanced"
        "Executive Interviews"
        "Sales Panel Interview",
        "Cross Team Interview",
        "CTO Interview",
        "Panel Interview",
        "Materials Demonstration",
    ),
    "offer": {("Offer")},
}

application = flask.Blueprint(
    "application",
    __name__,
    template_folder="/templates",
    static_folder="/dist",
)

session = talisker.requests.get_session()
harvest = Harvest(session=session, api_key=os.environ.get("HARVEST_API_KEY"))
cipher = Cipher(os.environ.get("APPLICATION_CRYPTO_SECRET_KEY"))
base_url = "https://harvest.greenhouse.io/v1"


# Helpers
# ===


def progressive(current, last):
    if current in milestone_stages:
        current_index = list(milestone_stages).index(current)
        last_index = list(milestone_stages).index(last)

        if current_index > last_index:
            return True
    return False


def _find_most_recent_milestone(stages):
    latest_milestone = next(iter(milestone_stages))
    for most_recent_finished_stage in reversed(stages):
        most_recent_finished_stage = most_recent_finished_stage.lower().strip()
        for milestone, stages_in_milestone in milestone_stages.items():
            for stage_in_milestone in stages_in_milestone:
                if (
                    stage_in_milestone.lower().strip()
                    == most_recent_finished_stage
                    and progressive(milestone, latest_milestone)
                ):
                    latest_milestone = milestone
    return latest_milestone


def _milestones_progress(current_stage, stages):
    """
    Get the list of finished and unfinished milestones for
    a given candidate's application

    - current_stage: (optional) The current stage that
    the candidate is currently in
    - stages: The list of job stages ordered in the chronological order
    """
    progress = {}
    if not current_stage:
        for milestone in milestone_stages:
            progress[milestone] = False
        return progress

    # Filter out todo stages that candidate hasn't done yet
    candidate_finished_stages = []
    stages = [stage["name"] for stage in stages]
    current_stage = current_stage["name"]
    for stage in stages:
        candidate_finished_stages.append(stage)
        if stage == current_stage:
            break

    most_recent_milestone = _find_most_recent_milestone(
        candidate_finished_stages
    )

    # Set the progress of all the milestones prior
    # to the current one as completed
    is_before_most_recent_milestone = bool(most_recent_milestone)
    for milestone in milestone_stages:
        progress[milestone] = is_before_most_recent_milestone
        if milestone == most_recent_milestone:
            is_before_most_recent_milestone = False

    return progress


def _get_application(application_id):
    application = harvest.get_application(int(application_id))
    job_post_id = application["job_post_id"]
    application["job_post"] = (
        harvest.get_job_post(job_post_id) if job_post_id else None
    )

    # Add candidate object
    application["candidate"] = harvest.get_candidate(
        application["candidate_id"]
    )

    # Retrieve hiring lead from first job
    job_id = application["jobs"][0]["id"]
    job = harvest.get_job(job_id)
    with open("webapp/hiring_leads.json") as json_file:
        application["hiring_leads_list"] = json.load(json_file)

    for recruiter in job["hiring_team"]["recruiters"]:
        if recruiter["responsible"]:
            application["hiring_lead"] = harvest.get_user(recruiter["id"])
            break

    stages = harvest.get_stages(job_id)

    # By default GH sends stages in the right order
    # we need to get the completed milestones based on the finished stages
    application["stage_progress"] = _milestones_progress(
        application["current_stage"], stages
    )

    # Retrieve scheduled interviews, calculate duration of each
    interviews_stage = {}
    for stage in stages:
        for interview in stage["interviews"]:
            interviews_stage[interview["id"]] = stage["name"]
    application["scheduled_interviews"] = harvest.get_interviews_scheduled(
        application["id"]
    )

    for interview in application["scheduled_interviews"]:
        interview["start"]["datetime"] = parse(interview["start"]["date_time"])
        interview["end"]["datetime"] = parse(interview["end"]["date_time"])
        difference = (
            interview["end"]["datetime"] - interview["start"]["datetime"]
        )
        interview["duration"] = int(difference.total_seconds() / 60)
        interview["stage_name"] = interviews_stage[
            interview["interview"]["id"]
        ]

    application["to_be_rejected"] = False

    if application["rejected_at"]:
        if not application["rejection_reason"]["type"]["id"] == 2:
            now = datetime.now(timezone.utc)
            rejection_time = parse(application["rejected_at"])
            time_after_rejection = int(
                (now - rejection_time).total_seconds() / 60
            )
            if time_after_rejection < 2880:
                application["to_be_rejected"] = True
            else:
                flask.abort(404)

    return application


def _get_application_from_token(token):
    token_application_id = cipher.decrypt(token)

    return _get_application(token_application_id)


def _confirmation_token(
    email, withdrawal_reason_id, withdrawal_message, application_id
):
    payload = {
        "email": email,
        "withdrawal_reason_id": withdrawal_reason_id,
        "withdrawal_message": withdrawal_message,
        "application_id": application_id,
    }
    token = json.dumps(payload)
    return cipher.encrypt(token)


def _send_mail(
    to_email,
    subject,
    message,
):
    # Get SMTP server configuration
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    smtp_sender_address = os.environ["SMTP_SENDER_ADDRESS"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_sender_address
    msg["To"] = ", ".join(to_email)
    msg.set_content(message, subtype="html")

    server = SMTP(smtp_server)

    if smtp_user and smtp_pass:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
    server.send_message(msg)
    server.quit()


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


@application.route("/faq")
def faq():
    return flask.render_template(
        "careers/application/faq.html",
    )


@application.route("/<string:token>")
def application_index(token):
    withdrawn = False
    application = _get_application_from_token(token)
    if application["status"] != "active" and application["rejection_reason"]:
        if application["rejection_reason"]["type"]["id"] == 2:
            withdrawn = True

    return flask.render_template(
        "careers/application/index.html",
        withdrawal_reasons=withdrawal_reasons,
        token=token,
        application=application,
        candidate=application["candidate"],
        withdrawn=withdrawn,
    )


@application.route("/withdraw/<string:token>")
def application_withdrawal(token):
    payload = json.loads(cipher.decrypt(token))
    application = _get_application(payload["application_id"])
    withdrawal_reason_id = payload.get("withdrawal_reason_id")
    withdrawal_message = payload.get("withdrawal_message")

    # call the Harvest API to reject the application
    response = harvest.reject_application(
        application["id"],
        application["hiring_lead"]["id"],
        withdrawal_reason_id,
        withdrawal_message,
    )
    response.raise_for_status()

    return flask.render_template("careers/application/withdrawal.html")


@application.route("/<string:token>", methods=["POST"])
def request_withdrawal(token):
    application = _get_application_from_token(token)

    # Sanitize and parse user input
    email = parseaddr(flask.request.form["email"])[1]
    candidate_email = parseaddr(
        application["candidate"]["email_addresses"][0]["value"]
    )[1]

    withdrawal_reason_id = flask.request.form["withdrawal-reason"]
    withdrawal_message = withdrawal_reasons[withdrawal_reason_id]

    if (
        withdrawal_reason_id == "33"
        and "withdrawal-reason-other" in flask.request.form
    ):
        withdrawal_message = flask.request.form["withdrawal-reason-other"]

    # Reject if user typed the wrong email
    if candidate_email != email:
        return flask.render_template(
            "careers/application/index.html",
            wrong_email=True,
            token=token,
            withdrawal_reasons=withdrawal_reasons,
            application=_get_application_from_token(token),
        )

    email_message = flask.render_template(
        "careers/application/_activate-email.html",
        applicant_name=application["candidate"]["first_name"],
        position=application["jobs"][0]["name"],
        hiring_lead=application["hiring_lead"],
        verification_link=_confirmation_token(
            candidate_email,
            withdrawal_reason_id,
            withdrawal_message,
            application["id"],
        ),
    )

    # In local development we usually don't have access to the SMTP server
    # This means in debug mode we skip sending the email.
    #
    # We want to make it very clear when sending has been skipped,
    # because it's easily conceivable that the production application
    # accidentally ends up in debug mode, or that the SMTP server isn't
    # properly set up in production.
    #
    # For this reason we should display on the confirmation page that we
    # didn't send the email.
    debug_skip_sending = flask.current_app.debug

    if not debug_skip_sending:
        _send_mail(
            to_email=[candidate_email],
            subject="Withdraw Application Confirmation",
            message=email_message,
        )
    return flask.render_template(
        "careers/application/index.html",
        debug_skip_sending=debug_skip_sending,
        email_message=email_message,
        candidate_email=candidate_email,
        token=token,
        withdrawal_requested=True,
        withdrawal_reasons=withdrawal_reasons,
        application=_get_application_from_token(token),
    )


@application.app_template_filter()
def job_location_countries(job_location):
    countries = []
    for region in regions:
        if region in job_location:
            for country in regions[region]:
                countries.append({"@type": "Country", "name": country})
    return countries
