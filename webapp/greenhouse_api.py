import base64
import json
import os
import re
import requests


from canonicalwebteam.http import CachedSession
from html import unescape


api_session = CachedSession(
    fallback_cache_duration=300, file_cache_directory=".webcache"
)

base_url = "https://boards-api.greenhouse.io/v1/boards/Canonical/jobs"


def get_vacancies(department):
    feed = api_session.get(f"{base_url}?content=true").json()
    path_department = remove_hyphens(department)
    vacancies = []
    for job in feed["jobs"]:
        feed_department = remove_hyphens(job["metadata"][2]["value"])
        if path_department.lower() == "all":
            vacancies.append(
                {
                    "title": job["title"],
                    "url": job["absolute_url"],
                    "location": job["location"]["name"],
                    "id": job["id"],
                    "employment": job["metadata"][0]["value"],
                    "date": job["metadata"][1]["value"],
                    "department": job["metadata"][2]["value"],
                    "management": job["metadata"][3]["value"],
                    "office": job["metadata"][4]["value"],
                }
            )
        elif path_department.lower() == feed_department.lower():
            vacancies.append(
                {
                    "title": job["title"],
                    "url": job["absolute_url"],
                    "location": job["location"]["name"],
                    "id": job["id"],
                    "employment": job["metadata"][0]["value"],
                    "date": job["metadata"][1]["value"],
                    "department": job["metadata"][2]["value"],
                    "management": job["metadata"][3]["value"],
                    "office": job["metadata"][4]["value"],
                }
            )
    return vacancies


def get_vacancy(job_id):
    feed = api_session.get(f"{base_url}/{job_id}").json()
    job = {
        "title": feed["title"],
        "content": unescape(feed["content"]),
        "location": feed["location"]["name"],
        "department": feed["metadata"][2]["value"],
    }
    return job


def submit_to_greenhouse(form_data, form_cv, job_id="1383152"):
    # Encode the API_KEY to base64
    API_KEY = os.environ["GREENHOUSE_API_KEY"]
    auth = (
        "Basic " + str(base64.b64encode(API_KEY.encode("utf-8")), "utf-8")[:-2]
    )
    # Encode the resume file to base64
    resume = base64.b64encode(form_cv["resume"].read()).decode("utf-8")
    # Create headers for api sumbission
    headers = {"Content-Type": "application/json", "Authorization": auth}
    # Create payload for api submission
    payload = json.dumps(
        {
            "first_name": form_data["first_name"],
            "last_name": form_data["last_name"],
            "email": form_data["email"],
            "phone": form_data["phone"],
            "resume_content": resume,
            "resume_content_filename": form_cv["resume"].filename,
        }
    )

    response = requests.post(
        f"{base_url}/{job_id}", data=payload, headers=headers
    )

    return response


def remove_hyphens(text):
    new_text = re.sub("-", "", text)
    return new_text
    