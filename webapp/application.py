import json
import os
import socket
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parseaddr
from functools import lru_cache
from smtplib import SMTP
from typing import Dict, List, Tuple
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import pytz
import logging


import flask
from dateutil.parser import parse

from webapp.greenhouse import HarvestV3
from webapp.job_regions import REGION_COUNTRIES
from webapp.utils.cipher import Cipher, InvalidToken
from webapp.google_calendar import CalendarAPI
from webapp.utils.constants import ONE_WEEK_IN_MINUTES, SECOND_LOOK_REQ_ID
from webapp.requests_session import get_requests_session_with_retries

logger = logging.getLogger(__name__)

OTHER_WITHDRAWAL_REASON_VALUE = "33"
LEGACY_OTHER_WITHDRAWAL_REASON_ID = "18"
OTHER_WITHDRAWAL_REJECTION_REASON_ID = "35818"

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
    OTHER_WITHDRAWAL_REASON_VALUE: "Other",
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

application_bp = flask.Blueprint(
    "application",
    __name__,
    template_folder="/templates",
    static_folder="/dist",
)

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


def _custom_field_values(custom_fields):
    return {
        key: field.get("value") if isinstance(field, dict) else field
        for key, field in (custom_fields or {}).items()
    }


def _job_summary(job):
    return {"id": job["id"], "name": job["name"]}


def _dashboard_status(status):
    return "active" if status == "in_process" else status


def _is_candidate_withdrawal(application):
    rejection_reason = application.get("rejection_reason") or {}
    rejection_type = rejection_reason.get("type") or {}
    return rejection_type.get("key") == "THEY_REJECTED_US"


def _resolve_withdrawal_reason(raw_reason_id, custom_message=None):
    """Normalise and validate a withdrawal reason id and its message."""
    reason_id = str(raw_reason_id) if raw_reason_id is not None else None
    if reason_id in {
        LEGACY_OTHER_WITHDRAWAL_REASON_ID,
        OTHER_WITHDRAWAL_REASON_VALUE,
    }:
        return (
            OTHER_WITHDRAWAL_REJECTION_REASON_ID,
            custom_message
            or withdrawal_reasons[OTHER_WITHDRAWAL_REASON_VALUE],
        )
    if reason_id not in withdrawal_reasons:
        flask.abort(400, "Invalid withdrawal reason")
    return reason_id, custom_message or withdrawal_reasons[reason_id]


def _get_related_applications(harvest, candidate):
    applications = harvest.get_applications(candidate["id"])
    job_ids = {app.get("job_id") for app in applications if app.get("job_id")}
    jobs = {job["id"]: job for job in harvest.get_jobs(job_ids)}

    related_applications = []
    for raw_application in applications:
        job = jobs.get(raw_application.get("job_id"))
        related_applications.append(
            {
                **raw_application,
                "status": _dashboard_status(raw_application["status"]),
                "custom_fields": _custom_field_values(
                    raw_application.get("custom_fields")
                ),
                "jobs": [_job_summary(job)] if job else [],
            }
        )

    candidate["applications"] = related_applications
    return jobs


@lru_cache(maxsize=1)
def _get_hiring_lead_videos():
    with open("webapp/hiring_leads.json") as json_file:
        return json.load(json_file)


def _get_hiring_lead(harvest, job_id):
    recruiters = harvest.get_job_owners(job_id, owner_type="recruiter")
    responsible_recruiter = next(
        (recruiter for recruiter in recruiters if recruiter["responsible"]),
        None,
    )
    if not responsible_recruiter:
        logger.warning("no responsible recruiter for job_id=%s", job_id)
        return None

    user = harvest.get_user(responsible_recruiter["user_id"])
    if not user:
        logger.warning(
            "responsible recruiter user is missing for job_id=%s", job_id
        )
        return None

    hiring_lead = {
        **user,
        "emails": [user["primary_email"]] if user.get("primary_email") else [],
        "bio": None,
        "avatar": None,
        "video_src": None,
    }

    employee_id = user.get("employee_id")
    if employee_id:
        try:
            employee_data = _get_employee_directory_data(employee_id)
            if employee_data["bio"]:
                hiring_lead["bio"] = employee_data["bio"].split("\\n")
        except Exception:
            logger.exception("failed to load hiring lead bio")

    hiring_lead_videos = _get_hiring_lead_videos()
    if job_id == 2680006:  # Enterprise Sales Representative
        hiring_lead["video_src"] = "https://www.youtube.com/embed/UvDSXgPbpt8"
    elif job_id == 2804114:  # Chief Revenue Officer
        hiring_lead["video_src"] = "https://www.youtube.com/embed/hO1rXwoRjx0"
    elif employee_id in hiring_lead_videos:
        hiring_lead["video_src"] = hiring_lead_videos[employee_id]["video_src"]

    return hiring_lead


def _get_calendar_interviews(
    harvest,
    application_id,
    job_id,
    job_stages,
    include_email=False,
):
    application_interviews = harvest.get_interviews(application_id)
    if not application_interviews:
        return []

    stages_by_id = {stage["id"]: stage for stage in job_stages}
    definitions_by_id = {
        interview["id"]: interview
        for interview in harvest.get_job_interviews(job_id)
    }

    interviews = []
    for interview in application_interviews:
        definition = definitions_by_id.get(interview["job_interview_id"])
        if not definition:
            logger.warning(
                "missing job interview definition for interview_id=%s",
                interview["id"],
            )
            continue
        if definition.get("scheduling_type") != "needs_scheduling":
            continue
        if not interview.get("starts_at") or not interview.get("ends_at"):
            continue
        interviews.append((interview, definition))

    interview_ids = [interview["id"] for interview, _ in interviews]
    panel_rows = harvest.get_interviewers(interview_ids)
    user_ids = {row.get("user_id") for row in panel_rows if row.get("user_id")}
    users_by_id = {user["id"]: user for user in harvest.get_users(user_ids)}
    panels_by_interview = {}
    for row in panel_rows:
        user = users_by_id.get(row.get("user_id"))
        interviewer = {
            "name": user["name"] if user else "Interviewer",
        }
        if include_email:
            interviewer["email"] = row.get("email") or (
                user.get("primary_email") if user else None
            )
        panels_by_interview.setdefault(row["interview_id"], []).append(
            interviewer
        )

    dashboard_interviews = []
    for interview, definition in interviews:
        start = parse(interview["starts_at"])
        end = parse(interview["ends_at"])
        stage = stages_by_id.get(definition["job_interview_stage_id"])
        dashboard_interviews.append(
            {
                **interview,
                "start": {
                    "date_time": interview["starts_at"],
                    "datetime": start,
                },
                "end": {"date_time": interview["ends_at"], "datetime": end},
                "duration": int((end - start).total_seconds() / 60),
                "interview": {
                    "id": definition["id"],
                    "name": definition["name"],
                },
                "stage_name": stage["name"] if stage else None,
                "interviewers": panels_by_interview.get(interview["id"], []),
            }
        )

    return sorted(
        dashboard_interviews,
        key=lambda interview: interview["start"]["datetime"],
    )


def _get_application(harvest, application_id, include_interviewer_email=False):
    application = harvest.get_application(int(application_id))
    if not application or application["status"] == "converted":
        flask.abort(404)

    application["status"] = _dashboard_status(application["status"])
    application["custom_fields"] = _custom_field_values(
        application.get("custom_fields")
    )
    application["custom_fields"].setdefault(
        "written_interview_submitted_at", None
    )

    job_post_id = application["job_post_id"]
    application["job_post"] = (
        harvest.get_job_post(job_post_id) if job_post_id else None
    )

    candidate = harvest.get_candidate(application["candidate_id"])
    if not candidate:
        flask.abort(404)
    jobs = _get_related_applications(harvest, candidate)
    application["candidate"] = candidate

    job_id = application["job_id"]
    job = jobs.get(job_id)
    if not job:
        flask.abort(404)
    application["jobs"] = [_job_summary(job)]
    application["hiring_lead"] = _get_hiring_lead(harvest, job_id)

    stages = sorted(
        harvest.get_job_interview_stages(job_id),
        key=lambda stage: stage["sort_order"],
    )
    application_stages = harvest.get_application_stages(application["id"])
    current_stage_id = next(
        (
            stage["job_interview_stage_id"]
            for stage in application_stages
            if stage["current"]
        ),
        None,
    )
    current_stage = next(
        (stage for stage in stages if stage["id"] == current_stage_id), None
    )
    if not current_stage and application.get("stage_name"):
        current_stage = next(
            (
                stage
                for stage in stages
                if stage["name"] == application["stage_name"]
            ),
            None,
        )
    application["current_stage"] = current_stage
    application["stage_progress"] = _milestones_progress(
        stages,
        current_stage,
    )

    application["scheduled_interviews"] = _get_calendar_interviews(
        harvest,
        application["id"],
        job_id,
        job_stages=stages,
        include_email=include_interviewer_email,
    )
    application["attachments"] = harvest.get_attachments(application["id"])
    application["to_be_rejected"] = False
    application["role_name"] = _calculate_job_title(application)
    application["rejection_reason"] = None

    if application.get("rejected_at"):
        rejection_details = harvest.get_rejection_details(application["id"])
        if rejection_details:
            rejection_reason_id = rejection_details.get("rejection_reason_id")
            if rejection_reason_id:
                application["rejection_reason"] = harvest.get_rejection_reason(
                    rejection_reason_id
                )
            if rejection_details.get("rejected_at"):
                application["rejected_at"] = rejection_details["rejected_at"]

        if not _is_candidate_withdrawal(application):
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


def _get_application_from_token(
    harvest, token, include_interviewer_email=False
):
    cipher = _get_cipher()
    token_application_id = cipher.decrypt(token)

    return _get_application(
        harvest,
        token_application_id,
        include_interviewer_email=include_interviewer_email,
    )


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
    smtp_port = os.getenv("SMTP_PORT")
    if smtp_port:
        smtp_port = int(smtp_port)

    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    smtp_sender_address = os.environ["SMTP_SENDER_ADDRESS"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_sender_address
    msg["To"] = ", ".join(to_email)
    msg.set_content(message, subtype="html")

    smtp_args = {
        "host": smtp_server,
        "timeout": 15,
    }
    if smtp_port:
        smtp_args["port"] = smtp_port

    server = SMTP(**smtp_args)
    if smtp_user and smtp_pass:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
    server.send_message(msg)
    server.quit()


@application_bp.after_request
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


@application_bp.route("/faq")
def faq():
    return flask.render_template(
        "careers/application/faq.html",
    )


@application_bp.route("/")
def application_access_denied():
    flask.abort(401, "No authentication token provided.")


@application_bp.route("/<string:token>")
def handle_application_index(token):
    with get_requests_session_with_retries() as session:
        harvest = HarvestV3.from_session(session)
        return application_index(harvest, token)


def application_index(harvest, token):
    withdrawn = False

    try:
        application = _get_application_from_token(harvest, token)
    except InvalidToken:
        flask.abort(401, "Invalid token")

    if application["status"] != "active":
        withdrawn = _is_candidate_withdrawal(application)

    gia_feedback = _get_gia_feedback(application["attachments"])
    if gia_feedback:
        application["gia_feedback"] = gia_feedback

    return flask.render_template(
        "careers/application/index.html",
        withdrawal_reasons=withdrawal_reasons,
        other_withdrawal_reason_value=OTHER_WITHDRAWAL_REASON_VALUE,
        token=token,
        application=application,
        candidate=application["candidate"],
        withdrawn=withdrawn,
        second_look_req_id=SECOND_LOOK_REQ_ID,
    )


@application_bp.route("/get-report/<string:token>", methods=["POST"])
def handle_application_report(token):
    with get_requests_session_with_retries() as session:
        harvest = HarvestV3.from_session(session)
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


def try_reject_interviews(application, applicant_name):
    try:
        candidate_interviews = [
            interview
            for interview in application["scheduled_interviews"]
            if interview["status"] == "awaiting_feedback"
            or (
                interview["status"] == "scheduled"
                and interview.get("external_event_id")
            )
        ]
        all_sent_emails = []

        calendar = CalendarAPI()
        for interview in candidate_interviews:
            can_be_deleted = False
            if interview["status"] == "scheduled":
                can_be_deleted = calendar.is_on_interview_calendar(
                    interview["external_event_id"]
                )
                if can_be_deleted:
                    delete_response = calendar.delete_interview_event(
                        event_id=interview["external_event_id"]
                    )

                    if delete_response:
                        logging.error(
                            "delete_interview_event " f"{delete_response=}"
                        )

                email_template = (
                    "careers/application/_withdrawal"
                    + "-interview-canceled-email.html"
                )
                email_title = (
                    "Interview Cancelation - "
                    + f"Candidate Withdrawal for {applicant_name}"
                )
            else:
                email_template = (
                    "careers/application/_withdrawal"
                    + "-feedback-not-needed-email.html"
                )
                email_title = (
                    "Interview Feedback - "
                    + f"Candidate Withdrawal for {applicant_name}"
                )

            interviewer = next(
                (
                    panel_member
                    for panel_member in interview["interviewers"]
                    if panel_member.get("email")
                ),
                None,
            )
            if not interviewer:
                logger.warning(
                    "no contactable interviewer for interview_id=%s",
                    interview["id"],
                )
                continue

            interviewer_timezone = calendar.get_timezone(interviewer["email"])
            interview_datetime_obj = interview["start"]["datetime"].astimezone(
                pytz.timezone(interviewer_timezone)
            )
            interview_date = interview_datetime_obj.strftime(
                "%B %d, %Y at %I:%M%p"
            )

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

            debug_skip_sending = flask.current_app.debug
            if not debug_skip_sending:
                _send_mail(
                    [interviewer["email"], "talent-mailbox@canonical.com"],
                    email_title,
                    email_for_interviewer,
                )

        return all_sent_emails
    except Exception:
        logger.exception("Error trying to reject interviews")
        return []


@application_bp.route("/withdraw/<string:token>")
def handle_application_withdrawal(token):
    with get_requests_session_with_retries() as session:
        harvest = HarvestV3.from_session(session)
        return application_withdrawal(harvest, token)


def application_withdrawal(harvest, token):
    try:
        cipher = _get_cipher()
        payload = json.loads(cipher.decrypt(token))
    except InvalidToken:
        flask.abort(401, "Invalid token")

    application = _get_application(
        harvest,
        payload["application_id"],
        include_interviewer_email=True,
    )
    withdrawal_reason_id, withdrawal_message = _resolve_withdrawal_reason(
        payload.get("withdrawal_reason_id"),
        payload.get("withdrawal_message"),
    )

    candidate_id = application["candidate"]["id"]

    hiring_lead = application.get("hiring_lead")
    hiring_lead_name = hiring_lead["name"] if hiring_lead else "Talent team"
    hiring_lead_email = (
        hiring_lead["emails"]
        if hiring_lead and hiring_lead["emails"]
        else ["talent-mailbox@canonical.com"]
    )

    applicant_name = (
        f"{application['candidate']['first_name']} "
        f"{application['candidate']['last_name']}"
    )

    application_url = (
        f"https://canonical.greenhouse.io/people/{candidate_id}?"
        f"application_id={payload['application_id']}"
    )

    response = harvest.reject_application(
        application["id"],
        withdrawal_reason_id,
        withdrawal_message,
    )
    response.raise_for_status()

    all_sent_emails = try_reject_interviews(application, applicant_name)

    email_message = flask.render_template(
        "careers/application/_withdrawal_notification-email.html",
        applicant_name=applicant_name,
        hiring_lead_name=hiring_lead_name,
        position=application["role_name"],
        application_url=application_url,
        current_stage=application["current_stage"] or {"name": "unknown"},
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


@application_bp.route("/<string:token>", methods=["POST"])
def handle_request_withdrawal(token):
    with get_requests_session_with_retries() as session:
        harvest = HarvestV3.from_session(session)
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

    raw_withdrawal_reason = flask.request.form["withdrawal-reason"]
    custom_message = (
        flask.request.form.get("withdrawal-reason-other")
        if raw_withdrawal_reason == OTHER_WITHDRAWAL_REASON_VALUE
        else None
    )
    withdrawal_reason_id, withdrawal_message = _resolve_withdrawal_reason(
        raw_withdrawal_reason,
        custom_message,
    )

    # Reject if user typed the wrong email
    if candidate_email != email:
        return flask.render_template(
            "careers/application/index.html",
            wrong_email=True,
            token=token,
            withdrawal_reasons=withdrawal_reasons,
            other_withdrawal_reason_value=OTHER_WITHDRAWAL_REASON_VALUE,
            application=application,
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
        other_withdrawal_reason_value=OTHER_WITHDRAWAL_REASON_VALUE,
        application=application,
    )


@application_bp.app_template_filter()
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
