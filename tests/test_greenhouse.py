import unittest

import importlib
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import requests
import json
from werkzeug.datastructures import MultiDict

import webapp.greenhouse as greenhouse
from webapp.greenhouse import (
    _payload_setup_mapped_url_token,
    _get_mapped_url_token,
    MappedUrlToken,
)


class TestGreenhouseDebugFlag(unittest.TestCase):
    def test_greenhouse_debug_logs_warning_when_enabled(self):
        """
        Test that a warning is logged when GREENHOUSE_DEBUG is set to true
        """
        with patch.dict(os.environ, {"GREENHOUSE_DEBUG": "true"}, clear=True):
            mock_logger = MagicMock()
            with patch.object(
                greenhouse.logging, "getLogger", return_value=mock_logger
            ):
                greenhouse_module = importlib.reload(greenhouse)

        mock_logger.warning.assert_called_once_with("GREENHOUSE_DEBUG=True")

        # Reset module state for other tests
        with patch.dict(os.environ, {}, clear=True):
            importlib.reload(greenhouse_module)


class TestGreenhouseAPI(unittest.TestCase):
    def test_parse_feed_department_not_matched(self):
        """
        Test that department slugs are generated correctly
        when no special cases apply
        """
        department = "foo"
        parsed_department = greenhouse.Department(department)
        self.assertEqual(parsed_department.slug, department)

    def test_parse_feed_department_matched(self):
        """
        Test that department slugs are generated correctly
        when special cases apply
        """
        # Check '&' and ' ' get replaced in slugs
        web_and_design = greenhouse.Department("Web & Design")
        self.assertEqual(web_and_design.slug, "web-and-design")

        # Check department renames are happening
        techops = greenhouse.Department("Techops")
        self.assertEqual(techops.slug, "support-engineering")

    def _build_job_payload(self, job_id="123"):
        """
        Helper function to build a job payload
        """
        return {
            "id": job_id,
            "title": "Senior Engineer",
            "metadata": [
                {"id": 186225, "value": "Management"},
                {"id": 149021, "value": "Full-time"},
                {"id": 2739136, "value": ["Engineering"]},
                {"id": 675557, "value": ["Python", "Go"]},
                {"id": 2739137, "value": "Job description"},
                {"id": 11961371, "value": True},
                {"id": 12679300, "value": False},
            ],
            "location": {"name": "Remote"},
            "content": "<p>Role</p>",
            "requisition_id": "REQ-1",
            "absolute_url": "https://example.com/job",
            "updated_at": "2024-01-01",
            "questions": [],
            "offices": [{"name": "Remote", "location": None}],
        }

    def test_get_vacancies_by_department_slug_filters(self):
        """
        Test that vacancies are filtered by department slug
        """
        gh = greenhouse.Greenhouse(session=MagicMock(), api_key="key")
        matching = MagicMock()
        matching.departments = [MagicMock(slug="engineering")]
        other = MagicMock()
        other.departments = [MagicMock(slug="marketing")]

        with patch.object(gh, "get_vacancies", return_value=[matching, other]):
            result = gh.get_vacancies_by_department_slug("engineering")

        self.assertEqual(result, [matching])

    def test_get_vacancies_by_skills_filters_and_sorts(self):
        """
        Test that vacancies are filtered and sorted by skills
        """
        gh = greenhouse.Greenhouse(session=MagicMock(), api_key="key")

        first = MagicMock(skills={"Go"})
        second = MagicMock(skills={"Python", "Terraform"})
        third = MagicMock(skills={"Python", "Go", "Terraform"})

        with patch.object(
            gh, "get_vacancies", return_value=[first, second, third]
        ):
            result = gh.get_vacancies_by_skills(["Python"])

        self.assertIn(third, result)
        self.assertIn(second, result)
        self.assertNotIn(first, result)

    def test_get_vacancy_primary_endpoint(self):
        """
        Test that vacancy is fetched from primary endpoint
        """
        session = MagicMock()
        job_payload = self._build_job_payload()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = job_payload
        session.get.return_value = response

        gh = greenhouse.Greenhouse(session=session, api_key="key")
        vacancy = gh.get_vacancy("123")

        session.get.assert_called_once_with(
            f"{gh.base_url}/123?questions=true", timeout=15
        )
        self.assertEqual(vacancy.id, "123")
        self.assertEqual(
            [dept.name for dept in vacancy.departments], ["Engineering"]
        )

    def test_get_vacancy_fallback_on_404(self):
        """
        Test that vacancy is fetched from fallback endpoint on 404
        """
        session = MagicMock()
        job_payload = self._build_job_payload("404-job")

        primary = MagicMock()
        primary.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=404)
        )
        fallback = MagicMock()
        fallback.raise_for_status.return_value = None
        fallback.json.return_value = job_payload
        session.get.side_effect = [primary, fallback]

        gh = greenhouse.Greenhouse(session=session, api_key="key")
        vacancy = gh.get_vacancy("404-job")

        self.assertEqual(session.get.call_count, 2)
        session.get.assert_called_with(
            f"{gh.canonicaljobs_url}/404-job?questions=true", timeout=15
        )
        self.assertEqual(vacancy.id, "404-job")

    def test_submit_application_builds_payload(self):
        """
        Test that application submission builds the correct payload
        """
        session = MagicMock()
        gh = greenhouse.Greenhouse(session=session, api_key="key", debug=False)

        form_data = MagicMock()
        form_data.to_dict.return_value = {"first_name": "Alice"}

        resume = MagicMock()
        resume.read.return_value = b"resume-bytes"
        resume.filename = "resume.pdf"

        cover = MagicMock()
        cover.read.return_value = b"cover-letter"
        cover.filename = "cover.txt"

        gh.submit_application(
            form_data=form_data,
            form_files={"resume": resume, "cover_letter": cover},
            job_id="999",
        )

        session.post.assert_called_once()
        kwargs = session.post.call_args.kwargs
        payload = json.loads(kwargs["data"])
        self.assertIn("resume_content", payload)
        self.assertIn("cover_letter_content", payload)
        self.assertEqual(payload["resume_content_filename"], "resume.pdf")
        self.assertEqual(payload["cover_letter_content_filename"], "cover.txt")

    def test_submit_application_preserves_multi_select_values(self):
        session = MagicMock()
        gh = greenhouse.Greenhouse(session=session, api_key="key", debug=False)
        form_data = MultiDict(
            [
                ("first_name", "Alice"),
                ("question_123[]", "10"),
                ("question_123[]", "20"),
            ]
        )

        gh.submit_application(
            form_data=form_data,
            form_files={},
            job_id="999",
        )

        payload = json.loads(session.post.call_args.kwargs["data"])
        self.assertEqual(payload["first_name"], "Alice")
        self.assertEqual(payload["question_123"], [10, 20])
        self.assertNotIn("question_123[]", payload)

    def test_submit_application_debug_short_circuits(self):
        """
        Test that application submission short-circuits when debug is enabled
        """
        session = MagicMock()
        gh = greenhouse.Greenhouse(session=session, api_key="key", debug=True)

        response = gh.submit_application(
            form_data=MagicMock(to_dict=lambda: {}),
            form_files={},
            job_id="111",
        )

        self.assertEqual(response.status_code, 200)
        session.post.assert_not_called()

    def test_get_mapped_url_token(self):
        token = _get_mapped_url_token(
            initial_referrer="https://canonical.com/",
            initial_url="https://canonical.com/careers/12345",
            utm_source=None,
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_DEFAULT)

        token = _get_mapped_url_token(
            initial_referrer="",
            initial_url="",
            utm_source=None,
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_DEFAULT)

        token = _get_mapped_url_token(
            initial_referrer="https://google.com/",
            initial_url="https://canonical.com/careers",
            utm_source=None,
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_GOOGLE_INDIRECT)

        token = _get_mapped_url_token(
            initial_referrer="https://google.com/",
            initial_url="https://canonical.com/careers/12345",
            utm_source=None,
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_GOOGLE_DIRECT)

        token = _get_mapped_url_token(
            initial_referrer="https://www.google.co.uk/",
            initial_url="https://canonical.com/careers",
            utm_source="smth",
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_GOOGLE_INDIRECT)

        token = _get_mapped_url_token(
            initial_referrer="https://www.google.co.uk/",
            initial_url="https://canonical.com/careers",
            utm_source="google_jobs_apply",
            job_id="12345",
        )
        self.assertEqual(token, MappedUrlToken.HOME_GOOGLE_JOBS)

    def test_payload_setup_mapped_url_token(self):
        payload = {}
        _payload_setup_mapped_url_token(
            payload=payload,
            initial_referrer="https://canonical.com/",
            initial_url="https://canonical.com/careers/12345",
            utm_source=None,
            job_id="12345",
        )
        self.assertDictEqual(
            payload, {"mapped_url_token": MappedUrlToken.HOME_DEFAULT}
        )

        payload = {}
        _payload_setup_mapped_url_token(
            payload=payload,
            initial_referrer="",
            initial_url="",
            utm_source=None,
            job_id="12345",
        )
        self.assertDictEqual(
            payload, {"mapped_url_token": MappedUrlToken.HOME_DEFAULT}
        )

        payload = {}
        _payload_setup_mapped_url_token(
            payload=payload,
            initial_referrer="https://google.com/",
            initial_url="https://canonical.com/careers",
            utm_source=None,
            job_id="12345",
        )
        self.assertDictEqual(
            payload, {"mapped_url_token": MappedUrlToken.HOME_GOOGLE_INDIRECT}
        )

        payload = {}
        _payload_setup_mapped_url_token(
            payload=payload,
            initial_referrer="https://google.com/",
            initial_url="https://canonical.com/careers/12345",
            utm_source=None,
            job_id="12345",
        )
        self.assertDictEqual(
            payload, {"mapped_url_token": MappedUrlToken.HOME_GOOGLE_DIRECT}
        )


class TestHarvestV3Auth(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.token_cache = greenhouse._HarvestV3TokenCache()
        self.auth = greenhouse.HarvestV3Auth(
            session=self.session,
            client_id="client-id",
            client_secret="client-secret",
            token_cache=self.token_cache,
        )

    def test_requests_and_caches_access_token(self):
        response = MagicMock()
        response.json.return_value = {
            "access_token": "token",
            "expires_in": 3600,
            "expires_at": "2000-01-01T00:00:00Z",
        }
        self.session.post.return_value = response

        self.assertEqual(self.auth.get_token(), "token")
        self.assertEqual(self.auth.get_token(), "token")
        self.assertGreater(
            self.token_cache.expires_at,
            datetime.now(timezone.utc) + timedelta(minutes=59),
        )

        self.session.post.assert_called_once_with(
            "https://auth.greenhouse.io/token",
            auth=("client-id", "client-secret"),
            params={"grant_type": "client_credentials"},
            json={},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        response.raise_for_status.assert_called_once()

    def test_refreshes_token_before_expiry(self):
        self.token_cache.token = "old-token"
        self.token_cache.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=30
        )
        response = MagicMock()
        response.json.return_value = {
            "access_token": "new-token",
            "expires_in": 3600,
        }
        self.session.post.return_value = response

        self.assertEqual(self.auth.get_token(), "new-token")

    def test_accepts_legacy_absolute_expiry(self):
        response = MagicMock()
        response.json.return_value = {
            "access_token": "token",
            "expires_at": "2099-01-01T00:00:00Z",
        }
        self.session.post.return_value = response

        self.assertEqual(self.auth.get_token(), "token")
        self.assertEqual(
            self.token_cache.expires_at,
            datetime(2099, 1, 1, tzinfo=timezone.utc),
        )

    def test_shares_cached_token_between_request_sessions(self):
        response = MagicMock()
        response.json.return_value = {
            "access_token": "shared-token",
            "expires_in": 3600,
        }
        self.session.post.return_value = response
        first_auth = greenhouse.HarvestV3Auth(
            session=self.session,
            client_id="shared-client-id",
            client_secret="client-secret",
        )
        other_session = MagicMock()
        other_auth = greenhouse.HarvestV3Auth(
            session=other_session,
            client_id="shared-client-id",
            client_secret="client-secret",
        )

        self.assertEqual(first_auth.get_token(), "shared-token")
        self.assertEqual(other_auth.get_token(), "shared-token")
        other_session.post.assert_not_called()


class TestHarvestV3(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.harvest = greenhouse.HarvestV3(
            session=self.session,
            client_id="client-id",
            client_secret="client-secret",
        )
        self.harvest._auth.get_token = MagicMock(return_value="token")

    def _mock_response(self, json_payload, status_code=200):
        response = MagicMock(status_code=status_code)
        response.json.return_value = json_payload
        response.links = {}
        return response

    def test_follows_cursor_pagination(self):
        first = self._mock_response([{"id": 1}])
        first.links = {
            "next": {
                "url": "https://harvest.greenhouse.io/v3/applications"
                "?cursor=next-cursor"
            }
        }
        second = self._mock_response([{"id": 2}])
        self.session.request.side_effect = [first, second]

        result = self.harvest._list("applications", job_ids=42, per_page=1)

        self.assertEqual(result, [{"id": 1}, {"id": 2}])
        self.assertEqual(
            self.session.request.call_args_list[1].kwargs["params"],
            {"cursor": "next-cursor"},
        )

    def test_get_application_uses_v3_list_filter(self):
        response = self._mock_response([{"id": 123}])
        self.session.request.return_value = response

        result = self.harvest.get_application("123")

        self.assertEqual(result, {"id": 123})
        self.session.request.assert_called_once_with(
            "GET",
            f"{self.harvest.base_url}applications",
            params={"ids": "123", "per_page": 500},
            json=None,
            headers={"Authorization": "Bearer token"},
            timeout=15,
        )
        response.raise_for_status.assert_called_once()

    def test_get_application_returns_none_when_missing(self):
        self.session.request.return_value = self._mock_response([])

        self.assertIsNone(self.harvest.get_application("123"))

    def test_get_application_rejects_mismatched_result(self):
        self.session.request.return_value = self._mock_response([{"id": 456}])

        with self.assertRaisesRegex(
            ValueError, "returned the wrong applications record"
        ):
            self.harvest.get_application("123")

    def test_get_rejection_details_verifies_application_id(self):
        details = {"id": 999, "application_id": 123}
        self.session.request.return_value = self._mock_response([details])

        self.assertEqual(self.harvest.get_rejection_details("123"), details)

    def test_serializes_parent_ids(self):
        response = self._mock_response([{"id": 1}])
        self.session.request.return_value = response

        result = self.harvest.get_interviewers({3, 2})

        self.assertEqual(result, [{"id": 1}])
        params = self.session.request.call_args.kwargs["params"]
        self.assertEqual(set(params["interview_ids"].split(",")), {"2", "3"})

    def test_retries_once_with_new_token_after_unauthorized(self):
        unauthorized = self._mock_response([], status_code=401)
        success = self._mock_response([{"id": 123}])
        self.session.request.side_effect = [unauthorized, success]
        self.harvest._auth.get_token.side_effect = ["old-token", "new-token"]
        self.harvest._auth.invalidate = MagicMock()

        result = self.harvest.get_application("123")

        self.assertEqual(result, {"id": 123})
        self.assertEqual(self.session.request.call_count, 2)
        self.harvest._auth.invalidate.assert_called_once()
        second_headers = self.session.request.call_args_list[1].kwargs[
            "headers"
        ]
        self.assertEqual(second_headers["Authorization"], "Bearer new-token")

    def test_reject_application(self):
        response = self._mock_response(None, status_code=204)
        self.session.request.return_value = response

        result = self.harvest.reject_application("1", "3", "note")

        self.assertIs(result, response)
        self.session.request.assert_called_once_with(
            "POST",
            f"{self.harvest.base_url}applications/1/reject",
            params=None,
            json={
                "rejection_reason_id": 3,
                "notes": "note",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer token",
            },
            timeout=30,
        )

    def test_reject_application_recovers_when_application_is_rejected(self):
        rejected_response = self._mock_response(None, status_code=422)
        error = requests.exceptions.HTTPError(response=rejected_response)
        rejected_response.raise_for_status.side_effect = error
        application_response = self._mock_response(
            [{"id": 1, "status": "rejected"}]
        )
        self.session.request.side_effect = [
            rejected_response,
            application_response,
        ]

        response = self.harvest.reject_application("1", "3", "note")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.session.request.call_count, 2)

    def test_reject_application_reraises_when_application_is_active(self):
        rejected_response = self._mock_response(None, status_code=422)
        error = requests.exceptions.HTTPError(response=rejected_response)
        rejected_response.raise_for_status.side_effect = error
        application_response = self._mock_response(
            [{"id": 1, "status": "in_process"}]
        )
        self.session.request.side_effect = [
            rejected_response,
            application_response,
        ]

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            self.harvest.reject_application("1", "3", "note")

        self.assertIs(context.exception, error)

    def test_reject_application_requires_reason(self):
        with self.assertRaisesRegex(
            ValueError, "rejection_reason_id is required"
        ):
            self.harvest.reject_application("1", None, "note")

        self.session.request.assert_not_called()

    def test_reject_application_normalizes_missing_notes(self):
        response = self._mock_response(None, status_code=204)
        self.session.request.return_value = response

        self.harvest.reject_application("1", "35818", None)

        payload = self.session.request.call_args.kwargs["json"]
        self.assertEqual(payload["notes"], "")

    @patch("webapp.greenhouse.logger")
    def test_reject_application_in_debug_mode(self, mock_logger):
        harvest = greenhouse.HarvestV3(
            session=self.session,
            client_id="client-id",
            client_secret="client-secret",
            debug=True,
        )

        response = harvest.reject_application("1", "3", "note")

        self.assertEqual(response.status_code, 204)
        self.session.request.assert_not_called()
        mock_logger.info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
