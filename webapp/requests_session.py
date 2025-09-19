import requests
from requests.adapters import HTTPAdapter, Retry
import talisker.requests


def get_requests_session():
    session = requests.Session()
    talisker.requests.configure(session)
    return session


def get_requests_session_with_retries():
    session = get_requests_session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        backoff_max=5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PATCH", "PUT"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session



