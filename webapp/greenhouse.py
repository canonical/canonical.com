# Standard library
import json
from base64 import b64encode

# Packages
from html import unescape


def _get_metadata(job, name):
    metadata_map = {
        "management": 186225,
        "employment": 149021,
        "department": 155450,
        "departments": 2739136,
        "skills": 675557,
        "description": 2739137,
        "employment_type": 149021,
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


class Department(object):
    def __init__(self, name):
        field = {
            "cloud engineering": "engineering",
            "device engineering": "engineering",
            "operations": "operations",
            "product management": "product",
        }

        self.name = name

        if name.lower() in field:
            self.slug = field[name.lower()]
        else:
            self.slug = name.replace("&", "and").replace(" ", "-").lower()


class Vacancy:
    def __init__(self, job: dict):
        self.id: str = job["id"]
        self.title: str = job["title"]
        self.meta_title: str = _get_meta_title(job)
        self.content: str = unescape(job["content"])
        self.url: str = job["absolute_url"]
        self.location: str = job["location"]["name"]
        self.employment: str = _get_metadata(job, "employment")
        self.date: str = job["updated_at"]
        self.questions: dict = job.get("questions", {})
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


class Greenhouse:
    def __init__(
        self,
        session,
        api_key,
        base_url="https://boards-api.greenhouse.io/v1/boards/Canonical/jobs",
    ):
        self.session = session
        self.base64_key = b64encode(f"{api_key}:".encode()).decode()
        self.base_url = base_url

    """
    Get all jobs from the API and parse them into vacancies
    Filter out vacancies without an office and a department
    """

    def get_vacancies(self):
        feed = self.session.get(f"{self.base_url}?content=true").json()

        vacancies = []

        for job in feed["jobs"]:
            # Filter out those without departments or offices
            if _get_metadata(job, "department") and job["offices"]:
                vacancies.append(Vacancy(job))

        return vacancies

    """
    Get vacancies where the department matches a given department slug
    """

    def get_vacancies_by_department_slug(self, department_slug):
        vacancies = self.get_vacancies()

        def department_filter(vacancy):
            for department in vacancy.departments:
                if department.slug == department_slug:
                    return True
            return False

        return list(filter(department_filter, vacancies))

    """
    Get vacancies containing any of a given list of skills
    Order by the number of matching skills, most first
    """

    def get_vacancies_by_skills(self, skills: list):
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

    """
    Retrieve a single job from Greenhouse by ID
    convert it to a Vacancy and return it
    """

    def get_vacancy(self, job_id):
        response = self.session.get(f"{self.base_url}/{job_id}?questions=true")

        response.raise_for_status()

        return Vacancy(response.json())

    """
    Default Job ID (1658196) is used below to submit CV without applying
    for a specific job
    https://boards-api.greenhouse.io/v1/boards/Canonical/jobs/1658196
    """

    def submit_application(self, form_data, form_files, job_id="1658196"):
        # Encode the resume file to base64
        resume = b64encode(form_files["resume"].read()).decode("utf-8")

        # Create payload for api submission
        payload = form_data.to_dict()
        payload["resume_content"] = resume
        payload["resume_content_filename"] = form_files["resume"].filename

        # Add cover letter to the payload if exists
        if form_files["cover_letter"]:
            # Encode the cover_letter file to base64
            payload["cover_letter_content"] = b64encode(
                form_files["cover_letter"].read()
            ).decode()
            payload["cover_letter_content_filename"] = form_files[
                "cover_letter"
            ].filename

        return self.session.post(
            f"{self.base_url}/{job_id}",
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.base64_key}",
            },
        )


class Harvest:
    def __init__(
        self, session, api_key, base_url="https://harvest.greenhouse.io/v1/"
    ):
        self.session = session
        self.base64_key = b64encode(f"{api_key}:".encode()).decode()
        self.base_url = base_url

    def get_departments(self):
        response = self.session.get(
            f"{self.base_url}custom_field/155450",
            headers={"Authorization": f"Basic {self.base64_key}"},
        )
        response.raise_for_status()
        departments = json.loads(response.text)["custom_field_options"]

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
        )
        response.raise_for_status()

        return response.json()

    def get_application(self, application_id):
        response = self.session.get(
            f"{self.base_url}applications/{application_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
        )
        response.raise_for_status()

        return response.json()

    def get_candidate(self, candidate_id):
        response = self.session.get(
            f"{self.base_url}candidates/{candidate_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
        )
        response.raise_for_status()

        return response.json()

    def get_job(self, job_id):
        response = self.session.get(
            f"{self.base_url}jobs/{job_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
        )
        response.raise_for_status()

        return response.json()

    def get_user(self, user_id):
        response = self.session.get(
            f"{self.base_url}users/{user_id}",
            headers={"Authorization": f"Basic {self.base64_key}"},
        )
        response.raise_for_status()

        return response.json()
