# Standard library
import base64
import json

# Packages
from html import unescape


base_url = "https://boards-api.greenhouse.io/v1/boards/Canonical/jobs"

metadata_map = {
    "management": 186225,
    "employment": 149021,
    "department": 155450,
    "skills": 675557,
}


def _parse_feed_department(feed_department):
    field = {
        "cloud engineering": "engineering",
        "device engineering": "engineering",
        "web and design": "design",
        "operations": "commercialops",
        "human resources": "hr",
    }

    if feed_department.lower() in field:
        return field[feed_department.lower()]

    return feed_department


class Greenhouse:
    def __init__(self, session):
        self.session = session

    def get_vacancies(self, department):
        feed = self.session.get(f"{base_url}?content=true").json()
        path_department = department.replace("-", "")
        vacancies = []
        for job in feed["jobs"]:
            if job["metadata"][2]["value"] and job["offices"]:
                feed_department = _parse_feed_department(
                    job["metadata"][2]["value"].replace("-", "")
                )
                if (
                    path_department.lower() == "all"
                    or path_department.lower() == feed_department.lower()
                ):
                    vacancies.append(
                        {
                            "title": job["title"],
                            "content": unescape(job["content"]),
                            "url": job["absolute_url"],
                            "location": job["location"]["name"],
                            "id": job["id"],
                            "employment": self.get_metadata_value(
                                job["metadata"], "employment"
                            ),
                            "date": job["updated_at"],
                            "department": self.get_metadata_value(
                                job["metadata"], "department"
                            ),
                            "management": self.get_metadata_value(
                                job["metadata"], "management"
                            ),
                            "office": job["offices"][0]["name"],
                        }
                    )
        return vacancies

    def get_vacancies_by_skills(self, core_skills):
        feed = self.session.get(f"{base_url}?content=true").json()
        vacancies = []
        for job in feed["jobs"]:
            job_core_skills = self.get_metadata_value(
                job["metadata"], "skills"
            )
            job_offices = ""
            if job["offices"]:
                job_offices = job["offices"][0]["name"]
            for skill in core_skills:
                if job_core_skills:
                    if skill in job_core_skills:
                        vacancies.append(
                            {
                                "title": job["title"],
                                "content": unescape(job["content"]),
                                "url": job["absolute_url"],
                                "location": job["location"]["name"],
                                "id": job["id"],
                                "employment": self.get_metadata_value(
                                    job["metadata"], "employment"
                                ),
                                "date": job["updated_at"],
                                "department": self.get_metadata_value(
                                    job["metadata"], "department"
                                ),
                                "management": self.get_metadata_value(
                                    job["metadata"], "management"
                                ),
                                "office": job_offices,
                                "core_skills": job_core_skills,
                            }
                        )
                        break

        return vacancies

    def get_metadata_value(self, job_metadata, metadata_key):
        for data in job_metadata:
            if data["id"] == metadata_map[metadata_key]:
                return data["value"]
        return None

    def get_vacancy(self, job_id):
        feed = self.session.get(f"{base_url}/{job_id}?questions=true").json()

        if feed.get("status") == 404:
            return None
        else:
            job = {
                "id": job_id,
                "title": feed["title"],
                "content": unescape(feed["content"]),
                "location": feed["location"]["name"],
                "department": feed["metadata"][2]["value"],
                "questions": feed["questions"],
            }
            return job

    # Default Job ID (1658196) is used below to submit CV without applying
    # for a specific job
    # https://boards-api.greenhouse.io/v1/boards/Canonical/jobs/1658196.
    def submit_application(
        self, api_key, form_data, form_files, job_id="1658196"
    ):
        if not api_key:
            raise AttributeError("No Greenhouse API key provided")

        # Encode the api_key to base64
        auth = (
            "Basic "
            + str(base64.b64encode(api_key.encode("utf-8")), "utf-8")[:-2]
        )
        # Encode the resume file to base64
        resume = base64.b64encode(form_files["resume"].read()).decode("utf-8")
        # Create headers for api sumbission
        headers = {"Content-Type": "application/json", "Authorization": auth}
        # Create payload for api submission
        payload = {
            "first_name": form_data["first_name"],
            "last_name": form_data["last_name"],
            "email": form_data["email"],
            "phone": form_data["phone"],
            "location": form_data["location"],
            "resume_content": resume,
            "resume_content_filename": form_files["resume"].filename,
        }

        # Add cover letter to the payload if exists
        if form_files["cover_letter"]:
            # Encode the cover_letter file to base64
            cover_letter = base64.b64encode(
                form_files["cover_letter"].read()
            ).decode("utf-8")
            payload["cover_letter_content"] = cover_letter
            payload["cover_letter_content_filename"] = form_files[
                "cover_letter"
            ].filename

        json_payload = json.dumps(payload)

        response = self.session.post(
            f"{base_url}/{job_id}", data=json_payload, headers=headers
        )

        return response

    def __department_category(sub_department):
        categories = {
            "engineering": [],
            "techops": [],
            "operations": [],
            "sales": ["data center sales", "dc inside sales", "dc inside sales - amer", "dc inside sales - emea / apac", "dc outside sales", "dc outside sales - amer", "dc outside sales - emea / apac"],
            "marketing": [],
            "web-and-design" : [],
            "project-management": ["dc project management"],
            "finance": [],
            "legal": ["advocacy"],
            "admin": [],
            "human-resources": []
        }

    def get_all_departments(self):
        feed = self.session.get(f"https://boards-api.greenhouse.io/v1/boards/Canonical/departments?content=true").json()
        departments = []
        for department in feed["departments"]:
            departments.append(department["name"])
        return departments

    def get_vacancy_department_slugs(self):
        vacancy_departments = []
        vacancies = self.get_vacancies("all")
        for vacancy in vacancies:
            vacancy_slug = _parse_feed_department(vacancy["department"]).lower().replace(" ", "-")
            if not (vacancy_slug in vacancy_departments):
                vacancy_departments.append(vacancy_slug)
        return vacancy_departments