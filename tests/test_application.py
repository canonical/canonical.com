import json
import unittest
from unittest.mock import MagicMock, patch
import flask

from vcr_unittest import VCRTestCase
from webapp.app import app
from webapp.application import (
    _milestones_progress,
    _sort_stages_by_milestone,
    _get_gia_feedback,
    _get_employee_directory_data,
    _submitted_email_match,
    application_withdrawal,
)
from webapp.greenhouse import Harvest
from webapp.utils.cipher import Cipher

all_stages = [
    {"name": "Application Review"},
    {"name": "Written Interview"},
    {"name": "Devskiller"},
    {"name": "Thomas International - GIA"},
    {"name": "Hold"},
    {"name": "Technical Exercise"},
    {"name": "Early Stage Interviews"},
    {"name": "Thomas International - PPA"},
    {"name": "Talent Interview"},
    {"name": "Late Stage Interviews"},
    {"name": "Shortlist"},
    {"name": "Executive Review"},
    {"name": "Offer"},
]


class TestApplicationPageHelpers(VCRTestCase):
    def _get_vcr_kwargs(self):
        """
        This removes the authorization header
        from VCR so we don't record auth parameters
        """
        return {"filter_headers": ["Authorization"]}

    def setUp(self):
        """
        Set up Flask app for testing
        """

        app.testing = True
        self.client = app.test_client()
        return super(TestApplicationPageHelpers, self).setUp()

    def test_sort_stages_by_milestone_sort_and_filter(self):
        milestones = {"m1": ["s1", "s2"], "m2": ["s3"]}
        stages_to_sort = ["s3", "s1", "s4", "s2", "s5"]
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            ["s1", "s2", "s3"],
        )

    def test_sort_stages_by_milestone_empty_stages(self):
        milestones = {"m1": ["s1", "s2"], "m2": ["s3"]}
        stages_to_sort = []
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            [],
        )

    def test_sort_stages_by_milestone_empty_milestones(self):
        milestones = {}
        stages_to_sort = ["s1", "s2"]
        self.assertListEqual(
            _sort_stages_by_milestone(stages_to_sort, milestones),
            [],
        )

    def test_milestone_progress_current_stage_defined(self):
        self.assertDictEqual(
            _milestones_progress(
                all_stages, {"name": "Early Stage Interviews"}
            ),
            {
                "application": True,
                "assessment": True,
                "early_stage": True,
                "late_stage": False,
                "offer": False,
            },
        )

    def test_milestone_progress_unordered_stages_list(self):
        all_stages = [
            {"name": "Offer"},
            {"name": "Application Review"},
            {"name": "Written Interview"},
            {"name": "Devskiller"},
            {"name": "Thomas International - GIA"},
            {"name": "Hold"},
            {"name": "Late Stage Interviews"},
            {"name": "Talent Interview"},
            {"name": "Technical Exercise"},
            {"name": "Early Stage Interviews"},
            {"name": "Shortlist"},
            {"name": "Thomas International - PPA"},
            {"name": "Executive Review"},
        ]
        self.assertDictEqual(
            _milestones_progress(all_stages, {"name": "Offer"}),
            {
                "application": True,
                "assessment": True,
                "early_stage": True,
                "late_stage": True,
                "offer": True,
            },
        )

    def test_milestone_progress_current_stage_undefined(self):
        self.assertDictEqual(
            _milestones_progress(all_stages, None),
            {
                "application": False,
                "assessment": False,
                "early_stage": False,
                "late_stage": False,
                "offer": False,
            },
        )

    def test_get_employee_directory_data(self):
        """
        When provided with a employee_id it should return
        an object with avatar, bio, email, id, name
        """
        fake_directory_data = {
            "avatar": "test_image",
            "bio": "test",
            "id": "1234",
            "name": "Mike Valen",
        }
        result = _get_employee_directory_data("1234")
        self.assertDictEqual(fake_directory_data, result)

    def test_job_post_page(self):
        """
        When given the /careers/<id> URL,
        we should return a 200 status code
        check requisition id is contained
        """
        response = self.client.get("/careers/4754075")
        self.assertEqual(response.status_code, 200)
        html_content = response.data.decode("utf-8")
        # Test Requistion ID is in the page
        self.assertIn("<p>Requisition ID: 613</p>", html_content)

    def test_cipher_encrypts_and_decrypts(self):
        cipher = Cipher("unit-test-secret")
        plaintext = "confidential data"
        encrypted = cipher.encrypt(plaintext)

        self.assertNotEqual(encrypted, plaintext)
        self.assertEqual(cipher.decrypt(encrypted), plaintext)


class TestGetGiaFeedback(unittest.TestCase):
    def test_gia_feedback_is_found_correctly(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        expected = [
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
        ]
        self.assertListEqual(_get_gia_feedback(attachments), expected)

    def test_gia_feedback_returns_all_if_more_available(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        expected = [
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
            {
                "filename": "Joe_Thomas_International_Candidate_Feedback.pdf",
                "url": "https://Thomas_International_Candidate_Feedback.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:19.012Z",
            },
        ]
        self.assertListEqual(_get_gia_feedback(attachments), expected)

    def test_gia_feedback_not_found(self):
        attachments = [
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:23.973Z",
            },
            {
                "filename": "Joe_Thomas_International_GIA_Report.pdf",
                "url": "https://Thomas_International_GIA_Report.pdf",
                "type": "other",
                "created_at": "2023-03-14T14:56:11.164Z",
            },
        ]
        self.assertEqual(_get_gia_feedback(attachments), [])

    def test_gia_feedback_not_found_when_empty(self):
        attachments = []
        self.assertEqual(_get_gia_feedback(attachments), [])


class TestCandidateEmailMatches(unittest.TestCase):
    def test_returns_correctly_for_single_email(self):
        application = {
            "candidate": {
                "email_addresses": [{"value": "a@b.com", "type": "personal"}]
            }
        }
        self.assertTrue(_submitted_email_match("a@b.com", application))
        self.assertFalse(_submitted_email_match("foo@bar.com", application))

    def test_returns_correctly_for_multiple_emails(self):
        application = {
            "candidate": {
                "email_addresses": [
                    {"value": "test@example.com", "type": "personal"},
                    {"value": "foo@bar.com", "type": "personal"},
                ]
            }
        }
        self.assertTrue(_submitted_email_match("foo@bar.com", application))
        self.assertFalse(_submitted_email_match("a@b.com", application))


class TestInterviewAutoDeletionOnWithdrawal(unittest.TestCase):
    def setUp(self):
        # fake constants
        self.fake_application = {
            "id": "123",
            "role_name": "Fake Job",
            "candidate": {
                "id": "444",
                "first_name": "John",
                "last_name": "Doe",
            },
            "hiring_lead": {
                "id": "777",
                "name": "Hiring Lead",
                "emails": "hiring_lead@example.com",
            },
            "current_stage": "Fake Stage",
        }
        self.fake_timezone = "America/Toronto"
        self.fake_scheduled_interview = {
            "status": "scheduled",  # should remain after filtering
            "interviewers": [
                {
                    "name": "Fake Interviewer 1",
                    "email": "fake_interviewer1@email.com",
                }
            ],
            "start": {"date_time": "2024-02-29T20:00:00.000Z"},
            "external_event_id": "fake_event_id_1",
            "interview": {"name": "Fake Interview 1"},
        }
        self.fake_completed_interview = {
            "status": "completed",  # should be filtered out
            "interviewers": [
                {
                    "name": "Fake Interviewer 2",
                    "email": "fake_interviewer2@email.com",
                }
            ],
            "start": {"date_time": "2024-02-27T20:00:00.000Z"},
            "external_event_id": "fake_event_id_2",
            "interview": {"name": "Fake Interview 2"},
        }
        self.fake_withdrawal_reason_id = None
        self.fake_withdrawal_message = None

        # mock functions
        self.mock_get_cipher = patch("webapp.application._get_cipher").start()
        self.mock_get_application = patch(
            "webapp.application._get_application"
        ).start()
        self.mock_render_template = patch(
            "webapp.application.flask.render_template"
        ).start()
        self.mock_cal = patch("webapp.application.CalendarAPI").start()
        self.mock_send_mail = patch("webapp.application._send_mail").start()
        self.mock_google_authenticate = patch(
            "webapp.google_calendar.CalendarAPI._authenticate"
        ).start()

        # set return values for mocks
        mock_cipher = MagicMock(spec=Cipher)
        mock_cipher.decrypt.return_value = json.dumps(
            {"application_id": self.fake_application["id"]}
        )
        self.mock_get_cipher.return_value = mock_cipher
        self.mock_get_application.return_value = self.fake_application
        self.mock_cal.return_value.get_timezone.return_value = (
            self.fake_timezone
        )
        self.mock_cal.return_value.delete_interview_event.return_value = None
        self.mock_cal.return_value.is_on_interview_calendar.return_value = True
        self.mock_send_mail.return_value = None
        self.mock_google_authenticate = None

        # create test context
        self.ctx = app.test_request_context()
        self.ctx.push()

        # set debug to true so we can test and ensure _send_mail is not called
        flask.current_app.debug = True

    def test_candidate_withdrawal_process(self):
        # call application_withdrawal function with a fake token
        mock_harvest = MagicMock(spec=Harvest)
        mock_harvest.reject_application.return_value = MagicMock(
            status_code=200
        )
        mock_harvest.get_interviews_scheduled.return_value = [
            self.fake_scheduled_interview,
            self.fake_completed_interview,
        ]
        application_withdrawal(mock_harvest, "fake_token")

        # ensure that get_interviews_scheduled was called with the right id
        mock_harvest.get_interviews_scheduled.assert_called_once_with(
            self.fake_application["id"]
        )

        # ensure that delete_interview_event only called once
        # (this asserts that the filtering worked, since only one of the
        # fake interviews has a status of "scheduled")
        self.mock_cal.return_value.delete_interview_event.assert_called_once()

        # ensure that delete_interview_event was called with
        # the correct argument
        self.mock_cal.return_value.delete_interview_event.assert_called_with(
            event_id=self.fake_scheduled_interview["external_event_id"]
        )

        # ensure _send_mail is not called (since debug is True)
        self.mock_send_mail.assert_not_called()

        # ensure get_timezone is called with correct email
        self.mock_cal.return_value.get_timezone.assert_called_with(
            self.fake_scheduled_interview["interviewers"][0]["email"]
        )

        # ensure datetime conversion worked
        expected_datetime = "February 29, 2024 at 03:00PM"
        _, kwargs = self.mock_render_template.call_args_list[0]
        self.assertIn("interview_date", kwargs)
        self.assertEqual(kwargs["interview_date"], expected_datetime)

        # ensure that harvest rejection fn is called with correct arguments
        mock_harvest.reject_application.assert_called_once_with(
            self.fake_application["id"],
            self.fake_application["hiring_lead"]["id"],
            self.fake_withdrawal_reason_id,
            self.fake_withdrawal_message,
        )

    def tearDown(self):
        # stop all of the patches from setUp
        patch.stopall()

        # pop the test context
        self.ctx.pop()


if __name__ == "__main__":
    unittest.main()
