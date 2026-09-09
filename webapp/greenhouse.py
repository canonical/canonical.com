# Standard library
import json
import os
import logging

from base64 import b64encode
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse
from threading import Lock
from urllib.parse import parse_qs, urlparse

# Packages
from html import unescape
import requests

logger = logging.getLogger(__name__)

GREENHOUSE_DEBUG = (
    os.environ.get("GREENHOUSE_DEBUG", "false").lower() != "false"
)


def _synthetic_response(status_code):
    """Build a response for a successful local outcome."""
    response = requests.Response()
    response.status_code = status_code
    return response


if GREENHOUSE_DEBUG:
    logger.warning(f"{GREENHOUSE_DEBUG=}")


def _get_metadata(job, name):
    metadata_map = {
        "management": 186225,
        "employment": 149021,
        "departments": 2739136,
        "skills": 675557,
        "description": 2739137,
        "employment_type": 149021,
        "is_featured": 11961371,
        "is_fast_track": 12679300,
        "discipline_track": 56835606,
    }

    for data in job["metadata"]:
        if data["id"] == metadata_map[name]:
            return data["value"]
    return None


def _get_meta_title(job):
    meta_title = job["title"].strip()
    if "Home" in job["location"]["name"]:
        meta_title += " - remote"
    else:
        meta_title += " in " + job["location"]["name"]

    return meta_title.replace("Office Based - ", "")


def _get_job_slug(job):
    # Sanitise title
    suffix = (
        job["title"]
        .encode("ascii", errors="ignore")
        .decode()
        .lower()
        .replace("/", "-")
        .replace(" ", "-")
        .replace("---", "-")
        .replace("--", "-")
        .replace(",", "")
        .replace("&", "and")
        .replace("(", "")
        .replace(")", "")
        .replace("-remote", "")
    )

    location = job["location"]["name"]

    if "home" in location.lower():
        location = "remote"

    return f"{suffix}-{location}"


def _add_req_to_content(job):
    # Add requisition ID to content
    if job["requisition_id"]:
        job["content"] = (
            job["content"]
            + "&lt;p&gt;Requisition ID: "
            + job["requisition_id"]
            + "&lt;p&gt;"
        )
    return unescape(job["content"])


class MappedUrlToken:
    HOME_DEFAULT = "tirwqhj81us"
    HOME_GOOGLE_DIRECT = "e4cnyg6y1us"
    HOME_GOOGLE_INDIRECT = "vph10yba1us"
    HOME_GOOGLE_JOBS = "2leak2sl1us"


_SECOND_LEVEL_LABELS = {"co", "com", "gov"}


def _extract_base_label(hostname: str) -> str:
    parts = hostname.split(".")
    if len(parts) == 1:
        return parts[0]

    if parts[-2] in _SECOND_LEVEL_LABELS and len(parts) >= 3:
        return parts[-3]

    return parts[-2]


def _get_mapped_url_token(
    initial_referrer: str | None,
    initial_url: str | None,
    utm_source: str | None,
    job_id: int | str,
) -> str | None:
    """mapped_url_token can be generated in jobboard configuration:
    https://canonical.greenhouse.io/jobboard
    """

    try:
        if utm_source == "google_jobs_apply":
            return MappedUrlToken.HOME_GOOGLE_JOBS

        if not initial_referrer:
            return MappedUrlToken.HOME_DEFAULT

        if initial_url is None:
            initial_url = ""

        direct = str(job_id) in initial_url
        parsed_referrer = urlparse(initial_referrer)
        referrer_hostname = (parsed_referrer.hostname or "").lower()
        if not referrer_hostname:
            return MappedUrlToken.HOME_DEFAULT

        base_label = _extract_base_label(referrer_hostname)

        if base_label == "google":
            if direct:
                return MappedUrlToken.HOME_GOOGLE_DIRECT
            return MappedUrlToken.HOME_GOOGLE_INDIRECT

        return MappedUrlToken.HOME_DEFAULT

    except Exception:
        logger.exception(
            "_get_mapped_url_token "
            f"{initial_referrer=} "
            f"{initial_url=} "
            f"{utm_source=} "
            f"{job_id=}"
        )
        return MappedUrlToken.HOME_DEFAULT


def _payload_setup_mapped_url_token(
    payload,
    initial_referrer,
    initial_url,
    utm_source,
    job_id,
):
    mapped_url_token = payload.get("mapped_url_token")
    if mapped_url_token:
        return

    payload.pop("mapped_url_token", None)
    mapped_url_token = _get_mapped_url_token(
        initial_referrer,
        initial_url,
        utm_source,
        job_id,
    )
    if not mapped_url_token:
        return

    payload["mapped_url_token"] = mapped_url_token


class Department(object):
    def __init__(self, name):
        self.name = name
        self.slug = name.replace("&", "and").replace(" ", "-").lower()

        # Rename some departments
        renames = {
            "techops": {
                "name": "Support Engineering",
                "slug": "support-engineering",
            },
            "human-resources": {"name": "People", "slug": "people"},
            "operations": {
                "name": "Commercial Operations",
                "slug": "commercial-operations",
            },
            "admin": {"name": "Administration", "slug": "administration"},
            "alliances": {
                "name": "Alliances & Channels",
                "slug": "alliances-and-channels",
            },
        }

        if self.slug in renames:
            self.name = renames[self.slug]["name"]
            self.slug = renames[self.slug]["slug"]


class Vacancy:
    def __init__(self, job: dict):
        self.id: str = job["id"]
        self.title: str = job["title"]
        self.meta_title: str = _get_meta_title(job)
        self.content: str = _add_req_to_content(job)
        self.url: str = job["absolute_url"]
        self.location: str = job["location"]["name"]
        self.employment: str = _get_metadata(job, "employment")
        self.date: str = job["updated_at"]
        self.questions: dict = self.parse_questions(job)
        self.departments: list = list(
            map(
                lambda d: Department(d),
                _get_metadata(job, "departments") or [],
            )
        )

        self.management: str = _get_metadata(job, "management")
        self.office: str = job["offices"][0]["name"]
        self.description: str = _get_metadata(job, "description")
        self.employment_type: str = _get_metadata(job, "employment_type")
        self.slug: str = _get_job_slug(job)
        self.skills: list = _get_metadata(job, "skills") or []
        self.featured: str = _get_metadata(job, "is_featured")
        self.fast_track: str = _get_metadata(job, "is_fast_track")
        self.discipline_track: str = _get_metadata(job, "discipline_track")

    def parse_questions(self, job):
        questions = job.get("questions", {})
        for question in questions:
            if question["description"]:
                question["description"] = (
                    question["description"]
                    .replace("</p>\n<p>", "<br />")
                    .replace("<p>", "")
                    .replace("</p>", "")
                )
        return questions

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "skills": self.skills,
            "url": self.url,
            "slug": self.slug,
            "management": self.management,
            "office": self.office,
            "description": self.description,
            "employment": self.employment,
            "date": self.date,
            "featured": self.featured,
            "fast_track": self.fast_track,
            "discipline_track": self.discipline_track,
            "departments": [dept.name for dept in self.departments],
        }


class Greenhouse:
    def __init__(
        self,
        session,
        api_key,
        base_url="https://boards-api.greenhouse.io/v1/boards/Canonical/jobs",
        canonicaljobs_url=(
            "https://boards-api.greenhouse.io/v1/boards/Canonicaljobs/jobs"
        ),
        debug=False,
    ):
        self.session = session
        self.base64_key = b64encode(f"{api_key}:".encode()).decode()
        self.base_url = base_url
        self.canonicaljobs_url = canonicaljobs_url
        self.debug = debug

    @staticmethod
    def from_session(session):
        greenhouse = Greenhouse(
            session=session,
            api_key=os.environ.get("GREENHOUSE_API_KEY"),
            debug=GREENHOUSE_DEBUG,
        )
        return greenhouse

    def get_vacancies(self):
        """
        Get all jobs from the API and parse them into vacancies
        Filter out vacancies without an office and a department
        """
        feed = self.session.get(
            f"{self.base_url}?content=true", timeout=15
        ).json()

        vacancies = []

        for job in feed["jobs"]:
            # Filter out those without departments or offices
            if _get_metadata(job, "departments") and job["offices"]:
                vacancies.append(Vacancy(job))

        return vacancies

    def get_vacancies_by_department_slug(self, department_slug):
        """
        Get vacancies where the department matches a given department slug
        """
        vacancies = self.get_vacancies()

        def department_filter(vacancy):
            for department in vacancy.departments:
                if department.slug == department_slug:
                    return True
            return False

        return list(filter(department_filter, vacancies))

    def get_vacancies_by_skills(self, skills: list):
        """
        Get vacancies containing any of a given list of skills
        Order by the number of matching skills, most first
        """
        vacancies = self.get_vacancies()

        # Remove non-matching jobs
        matching_vacancies = filter(
            lambda vacancy: bool(set(skills).intersection(vacancy.skills)),
            vacancies,
        )

        sorted_vacancies = sorted(
            matching_vacancies,
            key=lambda vacancy: len(set(skills).intersection(vacancy.skills)),
            reverse=True,
        )

        return sorted_vacancies

    def get_vacancy(self, job_id):
        """
        Retrieve a single job from Greenhouse by ID
        convert it to a Vacancy and return it.
        Tries the main board first, falls back to canonicaljobs board if
        not found.
        """
        # try main board first
        try:
            response = self.session.get(
                f"{self.base_url}/{job_id}?questions=true", timeout=15
            )
            response.raise_for_status()
            return Vacancy(response.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # try canonicaljobs board as fallback
                response = self.session.get(
                    f"{self.canonicaljobs_url}/{job_id}?questions=true",
                    timeout=15,
                )
                response.raise_for_status()
                return Vacancy(response.json())
            # re-raise any other HTTP errors
            raise

    def submit_application(self, form_data, form_files, job_id="1658196"):
        """
        Default Job ID (1658196) is used below to submit CV without applying
        for a specific job
        https://boards-api.greenhouse.io/v1/boards/Canonical/jobs/1658196
        """
        # Create payload for api submission
        payload = form_data.to_dict()

        for field_name in form_data.keys():
            if field_name.endswith("[]"):
                payload.pop(field_name, None)
                payload[field_name[:-2]] = [
                    int(value) for value in form_data.getlist(field_name)
                ]

        payload.pop("recaptcha_token", None)
        initial_referrer = payload.pop("initial_referrer", None)
        initial_url = payload.pop("initial_url", None)
        utm_source = payload.pop("utm_source", None)

        _payload_setup_mapped_url_token(
            payload,
            initial_referrer,
            initial_url,
            utm_source,
            job_id,
        )

        # Add resume to the payload if exists
        if form_files.get("resume"):
            # Encode the resume file to base64
            resume = b64encode(form_files["resume"].read()).decode("utf-8")
            payload["resume_content"] = resume
            payload["resume_content_filename"] = form_files["resume"].filename

        # Add cover letter to the payload if exists
        if form_files.get("cover_letter"):
            # Encode the cover_letter file to base64
            payload["cover_letter_content"] = b64encode(
                form_files["cover_letter"].read()
            ).decode()
            payload["cover_letter_content_filename"] = form_files[
                "cover_letter"
            ].filename

        if self.debug:
            resume_content = payload.get("resume_content") or ""
            cover_letter_content = payload.get("cover_letter_content") or ""
            payload["resume_content"] = f"{len(resume_content)=}"
            payload["cover_letter_content"] = f"{len(cover_letter_content)=}"
            logger.info(
                "SKIP submit_application "
                f"{initial_referrer=} "
                f"{initial_url=} "
                f"{payload=}"
            )
            response = requests.Response()
            response.status_code = 200
            return response

        return self.session.post(
            f"{self.base_url}/{job_id}",
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.base64_key}",
            },
            timeout=30,
        )


class _HarvestV3TokenCache:
    def __init__(self):
        self._lock = Lock()
        self.token = None
        self.expires_at = None

    def get_token(self, request_token):
        with self._lock:
            refresh_at = (
                self.expires_at - timedelta(seconds=60)
                if self.expires_at
                else None
            )
            if not self.token or datetime.now(timezone.utc) >= refresh_at:
                self.token, self.expires_at = request_token()
            return self.token

    def invalidate(self):
        with self._lock:
            self.token = None
            self.expires_at = None


_harvest_v3_token_caches = {}
_harvest_v3_token_caches_lock = Lock()


def _get_harvest_v3_token_cache(client_id):
    with _harvest_v3_token_caches_lock:
        token_cache = _harvest_v3_token_caches.get(client_id)
        if token_cache is None:
            token_cache = _HarvestV3TokenCache()
            _harvest_v3_token_caches[client_id] = token_cache
        return token_cache


class HarvestV3Auth:
    def __init__(self, session, client_id, client_secret, token_cache=None):
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret
        self._token_cache = token_cache or _get_harvest_v3_token_cache(
            client_id
        )

    def _request_token(self):
        response = self.session.post(
            "https://auth.greenhouse.io/token",
            auth=(self.client_id, self.client_secret),
            params={"grant_type": "client_credentials"},
            json={},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
        if "expires_in" in payload:
            expires_at = datetime.now(timezone.utc) + timedelta(
                seconds=payload["expires_in"]
            )
        else:
            expires_at = isoparse(payload["expires_at"])
        return (
            payload["access_token"],
            expires_at,
        )

    def invalidate(self):
        self._token_cache.invalidate()

    def get_token(self):
        return self._token_cache.get_token(self._request_token)


class HarvestV3:
    def __init__(
        self,
        session,
        client_id,
        client_secret,
        base_url="https://harvest.greenhouse.io/v3/",
        debug=False,
    ):
        self.session = session
        self.base_url = base_url
        self.debug = debug
        self._auth = HarvestV3Auth(
            session=self.session,
            client_id=client_id,
            client_secret=client_secret,
        )

    @staticmethod
    def from_session(session):
        return HarvestV3(
            session=session,
            client_id=os.environ.get("HARVEST_V3_CLIENT_ID"),
            client_secret=os.environ.get("HARVEST_V3_CLIENT_SECRET"),
            debug=GREENHOUSE_DEBUG,
        )

    def _request(
        self,
        method,
        path,
        params=None,
        json_body=None,
        headers=None,
        timeout=15,
    ):
        request_headers = dict(headers or {})

        def send_request():
            return self.session.request(
                method,
                f"{self.base_url}{path}",
                params=params,
                json=json_body,
                headers={
                    **request_headers,
                    "Authorization": f"Bearer {self._auth.get_token()}",
                },
                timeout=timeout,
            )

        response = send_request()
        if response.status_code == 401:
            self._auth.invalidate()
            response = send_request()

        response.raise_for_status()
        return response

    @staticmethod
    def _serialize_ids(ids):
        if isinstance(ids, (str, int)):
            return str(ids)
        return ",".join(str(item) for item in ids)

    def _list(self, resource, **params):
        params = {
            key: (
                self._serialize_ids(value)
                if key == "ids" or key.endswith("_ids")
                else value
            )
            for key, value in params.items()
            if value is not None
        }
        params.setdefault("per_page", 500)
        records = []
        seen_cursors = set()
        while True:
            response = self._request("GET", resource, params=params)
            records.extend(response.json())
            next_url = response.links.get("next", {}).get("url")
            if not next_url:
                return records
            cursor = parse_qs(urlparse(next_url).query).get("cursor", [None])[
                0
            ]
            if not cursor or cursor in seen_cursors:
                raise RuntimeError("invalid Harvest V3 pagination cursor")
            seen_cursors.add(cursor)
            params = {"cursor": cursor}

    def _get_one(
        self, resource, record_id, parameter="ids", record_id_field="id"
    ):
        records = self._list(resource, **{parameter: record_id})
        if not records:
            return None
        record = records[0]
        if str(record.get(record_id_field)) != str(record_id):
            raise ValueError(
                f"Harvest V3 returned the wrong {resource} record"
            )
        return record

    def _list_for_ids(self, resource, parameter, record_ids, **params):
        record_ids = sorted(record_ids)
        records = []
        for start in range(0, len(record_ids), 50):
            chunk = record_ids[start : start + 50]
            records.extend(
                self._list(resource, **{parameter: chunk}, **params)
            )
        return records

    def get_job_post(self, job_post_id):
        return self._get_one("job_posts", job_post_id)

    def get_application(self, application_id):
        return self._get_one("applications", application_id)

    def get_applications(self, candidate_id):
        return self._list("applications", candidate_ids=candidate_id)

    def get_candidate(self, candidate_id):
        return self._get_one("candidates", candidate_id)

    def get_jobs(self, job_ids):
        return self._list_for_ids("jobs", "ids", job_ids)

    def get_job_owners(self, job_id, owner_type=None):
        return self._list("job_owners", job_ids=job_id, type=owner_type)

    def get_user(self, user_id):
        return self._get_one("users", user_id)

    def get_users(self, user_ids):
        return self._list_for_ids("users", "ids", user_ids)

    def get_job_interview_stages(self, job_id):
        return self._list("job_interview_stages", job_ids=job_id)

    def get_application_stages(self, application_id):
        return self._list("application_stages", application_ids=application_id)

    def get_job_interviews(self, job_id):
        return self._list("job_interviews", job_ids=job_id)

    def get_interviews(self, application_id):
        return self._list("interviews", application_ids=application_id)

    def get_interviewers(self, interview_ids):
        return self._list_for_ids(
            "interviewers", "interview_ids", interview_ids
        )

    def get_attachments(self, application_id):
        return self._list("attachments", application_ids=application_id)

    def get_rejection_details(self, application_id):
        return self._get_one(
            "rejection_details",
            application_id,
            parameter="application_ids",
            record_id_field="application_id",
        )

    def get_rejection_reason(self, reason_id):
        return self._get_one("rejection_reasons", reason_id)

    def reject_application(self, application_id, rejection_reason_id, notes):
        """Reject an application through Harvest V3."""
        if rejection_reason_id is None:
            raise ValueError("rejection_reason_id is required")
        payload = {
            "rejection_reason_id": int(rejection_reason_id),
            "notes": notes or "",
        }

        if self.debug:
            logger.info(
                "SKIP reject_application "
                f"{application_id} {rejection_reason_id}"
            )
            return _synthetic_response(204)

        try:
            return self._request(
                "POST",
                f"applications/{application_id}/reject",
                json_body=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
        except requests.exceptions.HTTPError as error:
            if error.response is None or error.response.status_code != 422:
                raise

            # Harvest rejects an already-rejected application with a 422, so
            # confirm the post-condition before treating it as a real failure
            application = self.get_application(application_id)
            if not application or application.get("status") != "rejected":
                raise

            logger.warning(
                "Harvest V3 returned 422 after rejecting application_id=%s; "
                "treating the confirmed rejection as successful",
                application_id,
            )
            return _synthetic_response(204)
