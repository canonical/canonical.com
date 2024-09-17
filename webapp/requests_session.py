import requests
import talisker.requests


def get_requests_session():
    session = requests.Session()
    talisker.requests.configure(session)
    return session
