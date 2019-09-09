import re


from canonicalwebteam.http import CachedSession
from html import unescape


api_session = CachedSession(
    fallback_cache_duration=300, file_cache_directory=".webcache"
)


base_url = "https://api.greenhouse.io/v1/boards/Canonical/jobs"


# don't forget to handle errors
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
                }
            )
        elif path_department.lower() == feed_department.lower():
            vacancies.append(
                {
                    "title": job["title"],
                    "url": job["absolute_url"],
                    "location": job["location"]["name"],
                    "id": job["id"],
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


def remove_hyphens(text):
    new_text = re.sub("-", "", text)
    return new_text
