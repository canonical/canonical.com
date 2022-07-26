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
    )


@application.route("/withdrawal")
def application_withdrawal():
    return flask.render_template(
        "applications/withdrawal.html"
    )


import hashlib
secret_key = os.getenv("SECRET_KEY")

@application.route("/withdraw", methods = ['POST'])
def sendForm():
    email = flask.request.form['email']
    textarea = flask.request.form['textarea']

    print( email, textarea)
    return 


def confirmation_token(application_token):
    """Generate a unique secure token to be used as a way to
    confirm the candidate identity.

    Args:
        application_token (str): the application token (provided in `application_page(token)`)
    """
    print(secret_key + application_token)
    return (
        hashlib.sha256(
            (secret_key + application_token).encode("utf-8")
        ).hexdigest()
    )


import smtplib
from email.message import EmailMessage

# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
def send_mail(to_email, subject, message, server='smtp.gmail.com',
              from_email='xx@example.com'):
    # import smtplib
    try: 
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ', '.join(to_email)
        msg.set_content(message)
        print(msg)
        server = smtplib.SMTP(server)
        server.set_debuglevel(1)
        server.login(from_email, 'password')  # user & password
        server.send_message(msg)
        server.quit()
        print('successfully sent the mail.')
    except Exception:
        print('Error: unable to send email')

# # link = canonical.com/careers/withdraw/abcd-1234-db23-adfe
# send_mail(to_email=['min.kim@qq.com'],
#           subject='hello', message='Your analysis has done!')