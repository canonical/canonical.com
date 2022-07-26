import html
import json
import os
import smtplib
import socket
from email.message import EmailMessage
from email.utils import parseaddr
from flask import redirect
import flask
import talisker.requests
from dateutil.parser import parse

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
verification_token_cipher = Cipher(os.environ.get("SECRET_KEY"))


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
    milestone_stages = {
        "application": ("Application Review"),
        "assessment": (
            "Written Interview",
            "Psychometric Assessment",
            "Meet & Greet",
            "Hold",
        ),
        "early_stage": (
            "Early Stage Interviews",
            "Technical Exercise",
            "Technical Interview",
            "HR interview",
        ),
        "late_stage": (
            "Late Stage Interviews",
            "Shortlist",
            "Executive Review",
        ),
        "offer": ("Offer"),
    }

    progress = {}
    found = False
    for milestone, stages in milestone_stages.items():
        if current_stage in stages:
            progress[milestone] = True
            found = True
        elif not found:
            progress[milestone] = True
        else:
            progress[milestone] = False

    return progress


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
        token=token,
    )


@application.route("/withdraw/<string:token>")
def application_withdrawal(token):
    payload = verification_token_cipher.decrypt(token)
    try:
        payload = json.loads(payload)
        email = payload.get("email")
        withdrawal_reason = payload.get("withdrawal_reason", "")
        candidate_id = payload.get("candidate_id")
        application_id = payload.get("application_id")
    except (ValueError, TypeError):
        flask.abort(404)

    if not (email and candidate_id and application_id):
        flask.abort(404)

    application = harvest.get_application(application_id)
    candidate = harvest.get_candidate(application["candidate_id"])
    if (
        "candidate_id" not in application
        or application["candidate_id"] != candidate_id
    ):
        flask.abort(404)

    print(candidate["first_name"], withdrawal_reason)

    # TODO: call the Greenhouse API to reject the application here
    # ...
    return flask.render_template("applications/withdrawal.html")


@application.route("/withdraw/<string:token>", methods=["POST"])
def sendForm(token):
    decrypted = cipher.decrypt(token)
    if not decrypted:
        flask.abort(404)
    name, candidate_id, application_id = tuple(decrypted.split("-"))
    candidate_id, application_id = int(candidate_id), int(application_id)
    application = harvest.get_application(application_id)
    candidate = harvest.get_candidate(application["candidate_id"])
    if (
        "candidate_id" not in application
        or application["candidate_id"] != candidate_id
        or not candidate["first_name"].lower() == name
    ):
        flask.abort(404)

    candidate_name = candidate["first_name"]
    position = application["jobs"][0]["name"]

    # Sanitize and parse user input
    email = parseaddr(flask.request.form["email"])[1]
    candidate_email = parseaddr(candidate["email_addresses"][0]["value"])[1]
    textarea = html.escape(flask.request.form["textarea"])

    # Reject if user typed the wrong email
    if not candidate_email == email:
        flask.abort(404)

    send_mail(
        to_email=[candidate_email],
        subject="Withdraw Application Confirmation",
        message=flask.render_template(
            "applications/_activate-email.html",
            applicant_name=candidate_name,
            position=position,
            verification_link=confirmation_token(
                candidate_email, textarea, candidate_id, application_id
            ),
        ),
    )
    return redirect(flask.request.referrer + "#withdrawal-requested")


def confirmation_token(email, withdrawal_reason, candidate_id, application_id):
    payload = {
        "email": email,
        "withdrawal_reason": withdrawal_reason,
        "candidate_id": candidate_id,
        "application_id": application_id,
    }
    token = json.dumps(payload)
    return verification_token_cipher.encrypt(token)


def send_mail(
    to_email,
    subject,
    message,
    server="smtp.gmail.com",
    from_email="min.kim@canonical.com",
):
    # import smtplib
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(to_email)
        msg.set_content(message)

        server = smtplib.SMTP(server, 587)
        server.starttls()
        server.login(from_email, "")  # user & password
        server.send_message(msg)
        server.quit()
        print("successfully sent the email")
    except Exception:
        print("Error: unable to send email")
