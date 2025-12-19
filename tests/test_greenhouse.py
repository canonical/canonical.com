import unittest

import importlib
import os
from unittest.mock import MagicMock, patch

import requests
import json

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


class TestGreenhouseHarvest(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.harvest = greenhouse.Harvest(session=self.session, api_key="api")

    def _mock_response(self, *, json_payload=None, text_payload=None):
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        if json_payload is not None:
            resp.json.return_value = json_payload
        if text_payload is not None:
            resp.text = text_payload
        return resp

    def test_get_interviews_scheduled(self):
        """
        Test fetching scheduled interviews for an application
        """
        payload = [{"id": 1}]
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_interviews_scheduled("42")

        self.session.get.assert_called_once_with(
            f"{self.harvest.base_url}applications/42/scheduled_interviews",
            headers={"Authorization": f"Basic {self.harvest.base64_key}"},
            timeout=15,
        )
        self.assertEqual(result, payload)

    def test_get_application(self):
        """
        Test fetching an application by ID
        """
        payload = {"id": "123"}
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_application("123")

        self.assertEqual(result, payload)
        self.session.get.assert_called_once()
        self.session.get.return_value.raise_for_status.assert_called_once()

    def test_get_candidate(self):
        """
        Test fetching a candidate by ID
        """
        payload = {"id": "55"}
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_candidate("55")

        self.assertEqual(result, payload)
        self.session.get.assert_called_once_with(
            f"{self.harvest.base_url}candidates/55",
            headers={"Authorization": f"Basic {self.harvest.base64_key}"},
            timeout=15,
        )

    def test_get_job(self):
        """
        Test fetching a job by ID
        """
        payload = {"id": "78"}
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_job("78")

        self.assertEqual(result, payload)

    def test_get_stages(self):
        """
        Test fetching stages for a job
        """
        payload = [{"id": 1}]
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_stages("11")

        self.assertEqual(result, payload)
        self.session.get.assert_called_once_with(
            f"{self.harvest.base_url}jobs/11/stages",
            headers={"Authorization": f"Basic {self.harvest.base64_key}"},
            timeout=15,
        )

    def test_get_user(self):
        """
        Test fetching a user by ID
        """
        payload = {"id": "200"}
        self.session.get.return_value = self._mock_response(
            json_payload=payload
        )

        result = self.harvest.get_user("200")

        self.assertEqual(result, payload)

    @patch("webapp.greenhouse.logger")
    def test_reject_application(self, mock_logger):
        """
        Test rejecting an application
        """
        post_resp = MagicMock()
        self.session.post.return_value = post_resp

        response = self.harvest.reject_application("1", "2", "3", "note")

        self.assertIs(response, post_resp)
        self.session.post.assert_called_once_with(
            f"{self.harvest.base_url}applications/1/reject",
            json={
                "rejection_reason_id": "3",
                "notes": "note",
                "rejection_email": {"email_template_id": 348528},
            },
            headers={
                "Content-Type": "application/json",
                "On-Behalf-Of": "2",
                "Authorization": f"Basic {self.harvest.base64_key}",
            },
            timeout=30,
        )

    @patch("webapp.greenhouse.logger")
    def test_reject_application_in_debug_mode(self, mock_logger):
        """
        Test rejecting an application in debug mode
        """
        harvest = greenhouse.Harvest(
            session=self.session, api_key="api", debug=True
        )

        response = harvest.reject_application("1", "2", "3", "note")

        self.assertEqual(response.status_code, 200)
        self.session.post.assert_not_called()
        mock_logger.info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
