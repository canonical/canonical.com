import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def get_base_url():
    """
    Get and validate base URL from config.
    Raises ValueError if URL is not found.
    """
    base_url = current_app.config["CENTRAL_COOKIE_SERVICE_URL"]
    if not base_url:
        logger.error("CENTRAL_COOKIE_SERVICE_URL is not configured")
        raise ValueError("CENTRAL_COOKIE_SERVICE_URL is not configured")
    return base_url


def get_central_service_auth_headers():
    """
    Builds the auth headers.
    Raises ValueError if API key is not configured.
    """
    api_key = current_app.config.get("COOKIE_SERVICE_API_KEY")
    if not api_key:
        logger.error("COOKIE_SERVICE_API_KEY is not configured")
        raise ValueError("COOKIE_SERVICE_API_KEY is not configured")
    return {"Authorization": f"Bearer {api_key}"}


def exchange_code_for_uuid(code):
    """
    Exchanges the one-time code for a user_uuid at the central service.
    Returns None if the exchange fails.
    """
    try:
        url = f"{get_base_url()}/api/v1/token"
        headers = get_central_service_auth_headers()
        response = requests.post(
            url, headers=headers, json={"code": code}, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to exchange code for UUID: {e}")
        return None


def fetch_preferences(user_uuid):
    """
    Gets preferences from the central service.
    Returns None if the fetch fails.
    """
    try:
        url = f"{get_base_url()}/api/v1/users/{user_uuid}/preferences"
        headers = get_central_service_auth_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch preferences for user {user_uuid}: {e}")
        return None


def post_preferences(user_uuid, preferences):
    """
    Sets preferences at the central service.
    Returns None if the post fails.
    """
    try:
        url = f"{get_base_url()}/api/v1/users/{user_uuid}/preferences"
        headers = get_central_service_auth_headers()
        response = requests.post(
            url, headers=headers, json=preferences, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post preferences for user {user_uuid}: {e}")
        return None
