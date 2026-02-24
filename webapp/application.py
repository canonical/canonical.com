import json
import os
import socket
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parseaddr
from smtplib import SMTP
from typing import Dict, List, Tuple
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import pytz
import logging


import flask
from dateutil.parser import parse

from webapp.greenhouse import Harvest
from webapp.job_regions import REGION_COUNTRIES
from webapp.utils.cipher import Cipher, InvalidToken
from webapp.google_calendar import CalendarAPI
from webapp.utils.constants import ONE_WEEK_IN_MINUTES, SECOND_LOOK_REQ_ID
from webapp.requests_session import get_requests_session_with_retries

logger = logging.getLogger(__name__)

withdrawal_reasons = {
    "97001": "Accepted another offer – compensation",
    "97002": "Accepted another offer – role fit",
    "97004": (
        "I chose to remain with my current company "
        "as the timing/offer was a better fit"
    ),
    "97003": (
        "I chose to remain with my current company due to "
        "a new opportunity/promotion"
    ),
    "35818": "The position isn't a good fit",
    "36714": "I cannot complete the assessment",
    "33": "Other",
}

milestone_stages = {
    "application": ("Application Review",),
    "assessment": (
        "Written Interview",
        "Thomas International - GIA",
        "Psychometric Assessment",
        "Meet & Greet",
        "Peer Interview",
        "Phone Interview",
        "Domain Expert Screen",
        "ClassMarker",
        "Devskiller",
        "Technical Exercise",
    ),
    "early_stage": (
        "Early Stage Interviews",
        "Thomas International - PPA",
        "Take Home Test",
        "HR Interview",
        "Technical Interview",
        "Technical Assessment Classmarker",
        "Talent Interview",
        "Python Interview - Advanced",
    ),
    "late_stage": (
        "Exec Interview",
        "Reference Check",
        "Late Stage Interviews",
        "Executive Review",
        "Executive Interviews",
        "Sales Panel Interview",
        "Cross Team Interview",
        "CTO Interview",
        "Panel Interview",
        "Materials Demonstration",
    ),
    "offer": ("Offer",),
}

application = flask.Blueprint(
    "application",
    __name__,
    template_folder="/templates",
    static_folder="/dist",
)

base_url = "https://harvest.greenhouse.io/v1"

directory_api_url = "https://api.directory.canonical.com/graphql/"
directory_api_token = f'token {os.getenv("DIRECTORY_API_TOKEN", "")}'

# Helpers
# ===


def _get_cipher():
    cipher = Cipher(os.environ.get("APPLICATION_CRYPTO_SECRET_KEY", ""))
    return cipher


def _get_employee_directory_data(employee_id: str):
    """
    Get directory data of an employee given the
    employee_id
    """
    transport = RequestsHTTPTransport(
        url=directory_api_url,
        headers={"Authorization": directory_api_token},
        use_json=True,
        verify=False,
        timeout=5,
    )
    client = Client(transport=transport)
    filter_term = r"{id: $id}"
    query = gql(
        """
            query getEmployee($id: ID!){
                employees(filter:%s) {
                    id
                    name
                    bio
                }
            }
        """
        % filter_term
    )
    result = client.execute(query, variable_values={"id": employee_id}).get(
        "employees"
    )
    # It should always return 1 employee if employee_id is unique
    # and we have data consistency in the directory DB
    return result[0]


def _sort_stages_by_milestone(
    stages: List[str], milestones: Dict[str, Tuple[str]]
):
    """
    Sort the given stages by milestones and filter out not recognized ones
    - stages: the stages to sort
    - milestone: an order list of milestones as keys and
    sorted possible stages per milestone
    """
    stages = [stage for stage in stages]
    all_ordered_stages = [
        stage
        for stages_per_milestone in milestones.values()
        for stage in stages_per_milestone
    ]
    return [stage for stage in all_ordered_stages if stage in stages]


def _find_most_recent_milestone(stages: List[str]):
    """
    Search for the most recent milestone that the candidate is currently in
    """
    for most_recent_finished_stage in reversed(stages):
        most_recent_finished_stage = most_recent_finished_stage.lower().strip()
        for milestone, stages_in_milestone in milestone_stages.items():
            for stage_in_milestone in stages_in_milestone:
                if (
                    stage_in_milestone.lower().strip()
                    == most_recent_finished_stage
                ):
                    return milestone
    # return first milestone otherwise
    return next(iter(milestone_stages))


def _milestones_progress(stages, current_stage=None):
    """
    Get the list of finished and unfinished milestones for
    a given candidate's application

    - stages: The list of job stages ordered in the chronological order
    - current_stage: (optional) The current stage that the candidate is
    currently in
    """
    progress = {}
    if not current_stage:
        for milestone in milestone_stages:
            progress[milestone] = False
        return progress

    current_stage_id = current_stage["id"]

    # Filter out todo stages that candidate hasn't done yet
    candidate_finished_stages = []
    current_stage_found = False
    for stage in reversed(stages):
        if stage["id"] == current_stage_id:
            current_stage_found = True

        if current_stage_found:
            candidate_finished_stages.append(stage["name"])

    candidate_finished_stages = _sort_stages_by_milestone(
        candidate_finished_stages, milestone_stages
    )
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


def _calculate_job_title(application):
    """
    If the applied for job id matches the job post > job id then the job post
    title is the current role. If not the application has been transferred to
    another role so return that name.
    """
    if (
        application["job_post"]
        and application["jobs"][0]["id"] == application["job_post"]["job_id"]
    ):
        return application["job_post"]["title"]
    else:
        return application["jobs"][0]["name"]


def _get_application(harvest, application_id):
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

    for recruiter in job["hiring_team"]["recruiters"]:
        if recruiter["responsible"]:
            application["hiring_lead"] = harvest.get_user(recruiter["id"])
            application["hiring_lead"]["bio"] = None
            application["hiring_lead"]["avatar"] = None

            try:
                employee_data = _get_employee_directory_data(
                    recruiter["employee_id"]
                )
                if employee_data["bio"]:
                    application["hiring_lead"]["bio"] = employee_data[
                        "bio"
                    ].split("\\n")

            except Exception:
                logger.exception("failed to load hl bio")

            if job_id == 2680006:  # Enterprise Sales Representative
                application["hiring_lead"][
                    "video_src"
                ] = "https://www.youtube.com/embed/UvDSXgPbpt8"
            elif job_id == 2804114:  # Chief Revenue Officer
                application["hiring_lead"][
                    "video_src"
                ] = "https://www.youtube.com/embed/hO1rXwoRjx0"
            elif (
                # Currently only user with video
                # as we don't have a source to pull this video from
                # we still use the hiring_leads.json
                recruiter["employee_id"] == "4268"
                or recruiter["employee_id"] == "4289"
            ):
                with open("webapp/hiring_leads.json") as json_file:
                    hiring_lead_list = json.load(json_file)
                    application["hiring_lead"]["video_src"] = hiring_lead_list[
                        recruiter["employee_id"]
                    ]["video_src"]
            else:
                application["hiring_lead"]["video_src"] = None
            break

    stages = harvest.get_stages(job_id)

    # By default GH sends stages in the right order
    # we need to get the completed milestones based on the finished stages
    application["stage_progress"] = _milestones_progress(
        stages,
        application["current_stage"],
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

        # Remove private interviewer information
        interviewers = interview.get("interviewers")
        if interviewers is None:
            interviewers = []

        interview["interviewers"] = [{"name": i["name"]} for i in interviewers]

    application["to_be_rejected"] = False
    application["role_name"] = _calculate_job_title(application)

    if application["rejected_at"]:
        if not application["rejection_reason"]["type"]["id"] == 2:
            now = datetime.now(timezone.utc)
            rejection_time = parse(application["rejected_at"])
            time_after_rejection = int(
                (now - rejection_time).total_seconds() / 60
            )
            # candidate page should expire one week after rejection
            if time_after_rejection < ONE_WEEK_IN_MINUTES:
                application["to_be_rejected"] = True
            else:
                flask.abort(404)

    return application


def _get_application_from_token(harvest, token):
    cipher = _get_cipher()
    token_application_id = cipher.decrypt(token)

    return _get_application(harvest, token_application_id)


def _get_gia_feedback(attachments):
    feedback_attachments = []
    THOMAS_FILENAME = "Thomas_International_Candidate_Feedback.pdf"
    for attachment in attachments:
        if attachment["filename"] and attachment["filename"].endswith(
            THOMAS_FILENAME
        ):
            feedback_attachments.append(attachment)

    return feedback_attachments


def _submitted_email_match(submitted_email, application):
    candidate_emails_data = application["candidate"]["email_addresses"]
    candidate_emails_list = [a["value"] for a in candidate_emails_data]
    return submitted_email in candidate_emails_list


def _confirmation_token(
    email, withdrawal_reason_id, withdrawal_message, application_id
):
    cipher = _get_cipher()
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

    server = SMTP(host=smtp_server)
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


@application.route("/")
def application_access_denied():
    flask.abort(401, "No authentication token provided.")


@application.route("/<string:token>")
def handle_application_index(token):
    with get_requests_session_with_retries() as session:
        harvest = Harvest.from_session(session)
        return application_index(harvest, token)


def application_index(harvest, token):
    withdrawn = False

    try:
        application = _get_application_from_token(harvest, token)
    except InvalidToken:
        flask.abort(401, "Invalid token")

    if application["status"] != "active" and application["rejection_reason"]:
        if application["rejection_reason"]["type"]["id"] == 2:
            withdrawn = True

    gia_feedback = _get_gia_feedback(application["attachments"])
    if gia_feedback:
        application["gia_feedback"] = gia_feedback

    return flask.render_template(
        "careers/application/index.html",
        withdrawal_reasons=withdrawal_reasons,
        token=token,
        application=application,
        candidate=application["candidate"],
        withdrawn=withdrawn,
        second_look_req_id=SECOND_LOOK_REQ_ID,
    )


@application.route("/get-report/<string:token>", methods=["POST"])
def handle_application_report(token):
    with get_requests_session_with_retries() as session:
        harvest = Harvest.from_session(session)
        return application_report(harvest, token)


def application_report(harvest, token):
    try:
        application = _get_application_from_token(harvest, token)
    except InvalidToken:
        return flask.jsonify(
            {"status": "error", "message": "Could not find application"}
        )
    submitted_email = flask.request.json["request-assessment-email"]

    if not _submitted_email_match(submitted_email, application):
        return flask.jsonify(
            {
                "status": "error",
                "message": "The email you entered does not match the one "
                "from your application.",
            }
        )

    gia_feedback = _get_gia_feedback(application["attachments"])
    if gia_feedback:
        return flask.jsonify({"status": "success", "message": gia_feedback})


@application.route("/withdraw/<string:token>")
def handle_application_withdrawal(token):
    with get_requests_session_with_retries() as session:
        harvest = Harvest.from_session(session)
        return application_withdrawal(harvest, token)


def application_withdrawal(harvest, token):
    try:
        cipher = _get_cipher()
        payload = json.loads(cipher.decrypt(token))
    except InvalidToken:
        flask.abort(401, "Invalid token")

    application = _get_application(harvest, payload["application_id"])
    withdrawal_reason_id = payload.get("withdrawal_reason_id")
    withdrawal_message = payload.get("withdrawal_message")

    candidate_id = application["candidate"]["id"]

    hiring_lead_name = application["hiring_lead"]["name"]
    hiring_lead_email = application["hiring_lead"]["emails"]

    applicant_name = (
        f"{application['candidate']['first_name']} "
        f"{application['candidate']['last_name']}"
    )

    application_url = (
        f"https://canonical.greenhouse.io/people/{candidate_id}?"
        f"application_id={payload['application_id']}"
    )

    # get candidate interviews from Harvest API and filter
    candidate_interviews = harvest.get_interviews_scheduled(application["id"])
    candidate_interviews = [
        interview
        for interview in candidate_interviews
        if interview["status"] in ["scheduled", "awaiting_feedback"]
    ]
    all_sent_emails = []

    calendar = CalendarAPI()
    for interview in candidate_interviews:
        # get interviewer information
        interviewer = interview["interviewers"][0]
        interviewer_timezone = calendar.get_timezone(interviewer["email"])

        # convert interview time to interviewer's timezone
        interview_datetime_str = interview["start"]["date_time"]
        interview_datetime_obj = datetime.fromisoformat(
            interview_datetime_str.replace("Z", "+00:00")
        )
        interview_datetime_obj = interview_datetime_obj.astimezone(
            pytz.timezone(interviewer_timezone)
        )
        interview_date = interview_datetime_obj.strftime(
            "%B %d, %Y at %I:%M%p"
        )

        # if interview is still upcoming, we want to try to delete
        # the interview event
        can_be_deleted = False
        if interview["status"] == "scheduled":
            # can only delete interviews which are on the interview calendar
            # so we check this first
            can_be_deleted = calendar.is_on_interview_calendar(
                interview["external_event_id"]
            )
            if can_be_deleted:
                delete_response = calendar.delete_interview_event(
                    event_id=interview["external_event_id"]
                )

                # empty response is returned on successful deletion
                # so log error if not empty
                if delete_response:
                    logging.error(
                        "Delete response not empty, error deleting event:\n"
                        + str(delete_response)
                    )

            # email template and title for canceled interview
            email_template = (
                "careers/application/_withdrawal"
                + "-interview-canceled-email.html"
            )
            email_title = (
                "Interview Cancelation - "
                + f"Candidate Withdrawal for {applicant_name}"
            )
        else:
            # otherwise, set email template and title for feedback not needed
            email_template = (
                "careers/application/_withdrawal"
                + "-feedback-not-needed-email.html"
            )
            email_title = (
                "Interview Feedback - "
                + f"Candidate Withdrawal for {applicant_name}"
            )

        # build email to send to interviewer
        email_for_interviewer = flask.render_template(
            email_template,
            interviewer_name=interviewer["name"],
            interview_title=interview["interview"]["name"],
            applicant_name=applicant_name,
            interview_date=interview_date,
            position=application["role_name"],
            can_be_deleted=can_be_deleted,
        )
        all_sent_emails.append(
            {
                "interviewer": interviewer["email"],
                "message": email_for_interviewer,
            }
        )

        # send email
        debug_skip_sending = flask.current_app.debug
        if not debug_skip_sending:
            # also sending cancelation/feedback email to TS inbox
            # for tracking from their end.
            _send_mail(
                [interviewer["email"], "talent-mailbox@canonical.com"],
                email_title,
                email_for_interviewer,
            )

    # call the Harvest API to reject the application
    response = harvest.reject_application(
        application["id"],
        application["hiring_lead"]["id"],
        withdrawal_reason_id,
        withdrawal_message,
    )
    response.raise_for_status()

    email_message = flask.render_template(
        "careers/application/_withdrawal_notification-email.html",
        applicant_name=applicant_name,
        hiring_lead_name=hiring_lead_name,
        position=application["role_name"],
        hiring_lead=application["hiring_lead"],
        application_url=application_url,
        current_stage=application["current_stage"],
    )

    debug_skip_sending = flask.current_app.debug
    if not debug_skip_sending:
        _send_mail(
            hiring_lead_email,
            "Candidate Withdrawal for " + application["role_name"],
            email_message,
        )

    return flask.render_template(
        "careers/application/withdrawal.html",
        debug_skip_sending=debug_skip_sending,
        email_message=email_message,
        hiring_lead_email=hiring_lead_email,
        all_sent_emails=all_sent_emails,
    )


@application.route("/<string:token>", methods=["POST"])
def handle_request_withdrawal(token):
    with get_requests_session_with_retries() as session:
        harvest = Harvest.from_session(session)
        return request_withdrawal(harvest, token)


def request_withdrawal(harvest, token):
    try:
        application = _get_application_from_token(harvest, token)
    except InvalidToken:
        flask.abort(401, "Invalid token")

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
            application=_get_application_from_token(harvest, token),
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
        application=_get_application_from_token(harvest, token),
    )


@application.app_template_filter()
def job_location_countries(job_location_name: str):
    """
    locations as of 2025-12-02:
        Office Based - London, UK
        Home based - EMEA
        Home Based - Americas
        Office Based - Toronto, Canada
        Home based - Worldwide
        Office Based - Taipei, Taiwan
        Office Based - Beijing, China
        Home Based - APAC
    """

    if job_location_name is None:
        return []
    job_location_name = job_location_name.lower()
    if "home based" not in job_location_name:
        return []

    countries = []
    for region, region_countries in REGION_COUNTRIES.items():
        if region in job_location_name or "worldwide" in job_location_name:
            for country in region_countries:
                countries.append({"@type": "Country", "name": country})
    return countries
