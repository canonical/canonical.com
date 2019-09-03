import re

from canonicalwebteam.http import CachedSession


api_session = CachedSession(
    fallback_cache_duration=300, file_cache_directory=".webcache"
)

base_url = "https://api.greenhouse.io/v1/boards/Canonical/jobs"


def get_job_feed(endpoint):
    return api_session.get(f"{base_url}{endpoint}")


def get_vacancies(department):
    feed = get_job_feed('?content=true').json()
    path_department = remove_special_chars(department)
    vacancies = []
    for job in feed['jobs']:
        feed_department = remove_special_chars(job['metadata'][0]['value'])
        if path_department == 'all':
            vacancies.append({
                'title': job['title'],
                'url': job['absolute_url'],
                'location': job['location']['name'],
                'id': job['id'],
            })
        elif path_department == feed_department:
            vacancies.append({
                'title': job['title'],
                'url': job['absolute_url'],
                'location': job['location']['name'],
                'id': job['id'],
            })
    return vacancies


def remove_special_chars(text):
    new_text = re.sub('[^A-Za-z0-9]+', '', text.lower())
    return new_text
