# Standard library
import json
from base64 import b64encode
import os
import logging
from urllib.parse import urlparse

# Packages
from html import unescape
import requests


logger = logging.getLogger(__name__)


GREENHOUSE_DEBUG = (
    os.environ.get("GREENHOUSE_DEBUG", "false").lower() != "false"
)
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


def _get_mapped_url_token(
    initial_referrer: str | None,
    initial_url: str | None,
    job_id: int | str,
) -> str | None:
    """mapped_url_token can be generated in jobboard configuration:
    https://canonical.greenhouse.io/jobboard
    """

    try:
        if not initial_referrer:
            return MappedUrlToken.HOME_DEFAULT

        if initial_url is None:
            initial_url = ""

        direct = str(job_id) in initial_url
        parsed_referrer = urlparse(initial_referrer)
        referrer_hostname = (parsed_referrer.hostname or "").lower()
        if not referrer_hostname:
            return MappedUrlToken.HOME_DEFAULT

        initial_referrer_parts = referrer_hostname.split(".")
        if len(initial_referrer_parts) <= 1:
            return MappedUrlToken.HOME_DEFAULT

        if initial_referrer_parts[-2] == "google":
            if direct:
                return MappedUrlToken.HOME_GOOGLE_DIRECT
            return MappedUrlToken.HOME_GOOGLE_INDIRECT

        return MappedUrlToken.HOME_DEFAULT

    except Exception:
        logger.exception(
            "_get_mapped_url_token "
            f"{initial_referrer=} "
            f"{initial_url=} "
            f"{job_id=}"
        )
        return MappedUrlToken.HOME_DEFAULT


def _payload_setup_mapped_url_token(
    payload,
    initial_referrer,
    initial_url,
    job_id,
):
    mapped_url_token = payload.get("mapped_url_token")
    if mapped_url_token:
        return

    payload.pop("mapped_url_token", None)
    mapped_url_token = _get_mapped_url_token(
        initial_referrer, initial_url, job_id
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
        self.is_remote: bool = False if job["offices"][0]["location"] else True
        self.featured: str = _get_metadata(job, "is_featured")
        self.fast_track: str = _get_metadata(job, "is_fast_track")

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

        payload.pop("recaptcha_token", None)
        initial_referrer = payload.pop("initial_referrer", None)
        initial_url = payload.pop("initial_url", None)

        _payload_setup_mapped_url_token(
            payload, initial_referrer, initial_url, job_id
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


class Harvest:
    def __init__(
        self,
        session,
        api_key,
        base_url="https://harvest.greenhouse.io/v1/",
        debug=False,
    ):
        self.session = session
        self.base64_key = b64encode(f"{api_key}:".encode()).decode()
        self.base_url = base_url
        self.debug = debug

    @staticmethod
    def from_session(session):
        harvest = Harvest(
            session=session,
            api_key=os.environ.get("HARVEST_API_KEY"),
            debug=GREENHOUSE_DEBUG,
        )
        return harvest

    def get_departments(self):
        response = self.session.get(
            f"{self.base_url}custom_field/155450",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        departments = json.loads(response.text)["custom_field_options"]

        # Temporary fix until we move to new department list
        if not any(
            item["name"].lower() == "alliances" for item in departments
        ):
            departments.append({"id": 82559, "name": "Alliances"})

        return sorted(
            [Department(department["name"]) for department in departments],
            key=lambda dept: dept.name,
        )

    def get_interviews_scheduled(self, application_id):
        response = self.session.get(
            (
                f"{self.base_url}applications"
                f"/{application_id}/scheduled_interviews"
            ),
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()

        return response.json()

    def get_application(self, application_id):
        response = self.session.get(
            f"{self.base_url}applications/{application_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        response_json = response.json()
        response_id = response_json["id"]
        assert str(response_id) == str(
            application_id
        ), f"assert {application_id=} {response_id=}"
        return response_json

    def get_job_post(self, job_post_id):
        response = self.session.get(
            f"{self.base_url}job_posts/{job_post_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        response_json = response.json()
        response_id = response_json["id"]
        assert str(response_id) == str(
            job_post_id
        ), f"assert {job_post_id=} {response_id=}"
        return response_json

    def get_candidate(self, candidate_id):
        response = self.session.get(
            f"{self.base_url}candidates/{candidate_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        response_json = response.json()
        response_id = response_json["id"]
        assert str(response_id) == str(
            candidate_id
        ), f"assert {candidate_id=} {response_id=}"
        return response_json

    def get_job(self, job_id):
        response = self.session.get(
            f"{self.base_url}jobs/{job_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        response_json = response.json()
        response_id = response_json["id"]
        assert str(response_id) == str(
            job_id
        ), f"assert {job_id=} {response_id=}"
        return response_json

    def get_stages(self, job_id):
        response = self.session.get(
            f"{self.base_url}jobs/{job_id}/stages",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id):
        response = self.session.get(
            f"{self.base_url}users/{user_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
            timeout=15,
        )
        response.raise_for_status()
        response_json = response.json()
        response_id = response_json["id"]
        assert str(response_id) == str(
            user_id
        ), f"assert {user_id=} {response_id=}"
        return response_json

    def reject_application(
        self, application_id, user_id, rejection_reason_id, notes
    ):
        """Reject an application through Harvest API.
        https://developers.greenhouse.io/harvest.html#post-reject-application
        :param application_id: the id of the application to be rejected
        :param user_id: the greenhouse id of the user performing the rejection
        :param body: optional parameters (e.g. rejection reason)
        :returns: the id of the application rejected,
        if the request is successful, otherwise it raises an error
        """

        payload = {
            "rejection_reason_id": rejection_reason_id,
            "notes": notes,
            "rejection_email": {"email_template_id": 348528},
        }

        if self.debug:
            logger.info(
                "SKIP reject_application "
                f"{application_id} {user_id} {rejection_reason_id}"
            )
            response = requests.Response()
            response.status_code = 200
            return response

        response = self.session.post(
            f"{self.base_url}applications/{application_id}/reject",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "On-Behalf-Of": f"{user_id}",
                "Authorization": f"Basic {self.base64_key}",
            },
            timeout=30,
        )

        return response
