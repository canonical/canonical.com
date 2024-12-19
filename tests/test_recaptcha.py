import unittest
import requests
import responses
from webapp.recaptcha import verify_recaptcha


class TestRecaptcha(unittest.TestCase):
    @responses.activate
    def test_verify_recaptcha_enabled_pass(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_score(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.8,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertFalse(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_action(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION_BAD",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertFalse(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_invalid(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": False,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertFalse(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_big_token(self):
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf" * 100, "TEST_ACTION", recaptcha_config
        )
        self.assertFalse(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_no_token(self):
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, None, "TEST_ACTION", recaptcha_config
        )
        self.assertFalse(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_enabled_exception(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            body=requests.exceptions.Timeout,
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": True,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_pass(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_score(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.8,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_action(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": True,
                    "action": "TEST_ACTION_BAD",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_invalid(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            json={
                "tokenProperties": {
                    "valid": False,
                    "action": "TEST_ACTION",
                },
                "riskAnalysis": {
                    "score": 0.9,
                },
            },
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_big_token(self):
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf" * 100, "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_no_token(self):
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, None, "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)

    @responses.activate
    def test_verify_recaptcha_disabled_exception(self):
        url = (
            "https://recaptchaenterprise.googleapis.com/v1/projects/"
            "project-id-001/assessments?key=api-key-001"
        )
        responses.post(
            url,
            body=requests.exceptions.Timeout,
        )
        session = requests.Session()
        recaptcha_config = {
            "enabled": False,
            "site_key": "site-key-001",
            "project_id": "project-id-001",
            "api_key": "api-key-001",
            "score_threshold": 0.9,
            "max_token_size": 100,
        }
        recaptcha_passed = verify_recaptcha(
            session, "asdf", "TEST_ACTION", recaptcha_config
        )
        self.assertTrue(recaptcha_passed)
