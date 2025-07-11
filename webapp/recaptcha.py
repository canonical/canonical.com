import logging
import os

logger = logging.getLogger(__name__)


def load_recaptcha_config() -> dict:
    config = {
        "enabled": os.getenv("RECAPTCHA_ENABLED", "false").lower() != "false",
        "site_key": os.getenv("RECAPTCHA_SITE_KEY"),
        "project_id": os.getenv("RECAPTCHA_PROJECT_ID"),
        "api_key": os.getenv("RECAPTCHA_API_KEY"),
        "score_threshold": float(
            os.getenv("RECAPTCHA_SCORE_THRESHOLD", "0.5"),
        ),
        "max_token_size": 100000,
    }
    msg = (
        "RECAPTCHA "
        f"enabled={config['enabled']} "
        f"score_threshold={config['score_threshold']}",
    )
    logger.info(msg)

    return config


def verify_recaptcha(
    session,
    recaptcha_token,
    expected_action,
    recaptcha_config=None,
):
    # interpreting assesment:
    # https://cloud.google.com/recaptcha/docs/interpret-assessment-website
    try:
        if recaptcha_config is None:
            recaptcha_config = load_recaptcha_config()

        enabled = recaptcha_config["enabled"]
        site_key = recaptcha_config["site_key"]
        project_id = recaptcha_config["project_id"]
        api_key = recaptcha_config["api_key"]
        score_threshold = recaptcha_config["score_threshold"]
        max_token_size = recaptcha_config["max_token_size"]

        if recaptcha_token is None:
            logger.debug("recaptcha_token is None")
            return not enabled

        if len(recaptcha_token) > max_token_size:
            logger.debug("len(recaptcha_token) > RECAPTCHA_MAX_TOKEN_SIZE")
            # a large token can be forged to trigger a timeout
            return not enabled

        verify_url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            f"{project_id}/assessments?key={api_key}"
        )
        response = session.post(
            verify_url,
            json={
                "event": {
                    "token": recaptcha_token,
                    "expectedAction": expected_action,
                    "siteKey": site_key,
                },
            },
            timeout=30,
        )
        response.raise_for_status()
        assessment = response.json()

        token_valid = assessment["tokenProperties"]["valid"]
        if not token_valid:
            logger.debug("not token_valid")
            return not enabled

        token_action = assessment["tokenProperties"]["action"]
        if token_action != expected_action:
            logger.debug(f"{token_action=} {expected_action=}")
            return not enabled

        token_score = assessment["riskAnalysis"]["score"]
        if token_score < score_threshold:
            logger.debug(f"{score_threshold=} {token_score=}")
            return not enabled

        return True

    except Exception:
        logger.exception("verify_recaptcha")
        # do not restrict in case of error in the implementation
        return True
