import json
import unittest
import os
from unittest.mock import MagicMock, patch
import flask

from vcr_unittest import VCRTestCase
from webapp.app import app
from webapp.application import (
    _confirmation_token,
    _get_application,
    _get_application_from_token,
    _get_cipher,
    _get_gia_feedback,
    _get_employee_directory_data,
    _milestones_progress,
    _send_mail,
    _sort_stages_by_milestone,
    _submitted_email_match,
    application_withdrawal,
    job_location_countries,
)
from webapp.greenhouse import Harvest
from webapp.utils.cipher import Cipher, InvalidToken

all_stages = [
    {"id": 1, "name": "Application Review"},
    {"id": 2, "name": "Written Interview"},
    {"id": 3, "name": "Devskiller"},
    {"id": 4, "name": "Thomas International - GIA"},
    {"id": 5, "name": "Hold"},
    {"id": 6, "name": "Technical Exercise"},
    {"id": 7, "name": "Early Stage Interviews"},
    {"id": 8, "name": "Thomas International - PPA"},
    {"id": 9, "name": "Talent Interview"},
    {"id": 10, "name": "Late Stage Interviews"},
    {"id": 11, "name": "Shortlist"},
    {"id": 12, "name": "Executive Review"},
    {"id": 13, "name": "Offer"},
]


class TestApplicationPageHelpers(VCRTestCase):
    def _get_vcr_kwargs(self):
        """
        This removes the authorization header
        from VCR so we don't record auth parameters
        """
        return {
            "filter_headers": ["Authorization"],
            # Our cassettes include gzip-compressed response bodies.
            # Enable transparent decoding during playback so callers can
            # safely call `response.json()`.
            "decode_compressed_response": True,
        }

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
                all_stages, {"id": 7, "name": "Early Stage Interviews"}
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
            {"id": 13, "name": "Offer"},
            {"id": 1, "name": "Application Review"},
            {"id": 2, "name": "Written Interview"},
            {"id": 3, "name": "Devskiller"},
            {"id": 4, "name": "Thomas International - GIA"},
            {"id": 5, "name": "Hold"},
            {"id": 10, "name": "Late Stage Interviews"},
            {"id": 9, "name": "Talent Interview"},
            {"id": 6, "name": "Technical Exercise"},
            {"id": 7, "name": "Early Stage Interviews"},
            {"id": 11, "name": "Shortlist"},
            {"id": 8, "name": "Thomas International - PPA"},
            {"id": 12, "name": "Executive Review"},
        ]
        self.assertDictEqual(
            _milestones_progress(all_stages, {"id": 13, "name": "Offer"}),
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

    def test_milestone_progress_duplicate_hold_uses_stage_id_anchor(self):
        stages = [
            {"id": 1, "name": "Application Review"},
            {"id": 2, "name": "Written Interview"},
            {"id": 3, "name": "Hold"},
            {"id": 4, "name": "Technical Exercise"},
            {"id": 5, "name": "Hold"},
            {"id": 6, "name": "Early Stage Interviews"},
            {"id": 7, "name": "Talent Interview"},
            {"id": 8, "name": "Hold"},
        ]

        # candidate is in the middle "Hold" (assessment section), not the
        # final "Hold" (after early-stage interviews).
        self.assertDictEqual(
            _milestones_progress(stages, {"id": 5, "name": "Hold"}),
            {
                "application": True,
                "assessment": True,
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
        """
        Ensure that the Cipher class can
        encrypt and decrypt data correctly
        """
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


class TestGetCipher(unittest.TestCase):
    def test_get_cipher_uses_env_secret(self):
        """
        Ensure that _get_cipher uses the
        APPLICATION_CRYPTO_SECRET_KEY environment variable
        """
        with patch.dict(
            os.environ,
            {"APPLICATION_CRYPTO_SECRET_KEY": "test-key"},
            clear=True,
        ):
            with patch("webapp.application.Cipher") as mock_cipher:
                cipher_instance = mock_cipher.return_value
                result = _get_cipher()

        mock_cipher.assert_called_once_with("test-key")
        self.assertIs(result, cipher_instance)

    def test_get_cipher_defaults_to_empty_secret(self):
        """
        Ensure that _get_cipher defaults to
        an empty string when APPLICATION_CRYPTO_SECRET_KEY
        is not set
        """
        with patch.dict(os.environ, {}, clear=True):
            with patch("webapp.application.Cipher") as mock_cipher:
                _get_cipher()

        mock_cipher.assert_called_once_with("")


class TestGetApplication(unittest.TestCase):
    def setUp(self):
        self.app_ctx = app.app_context()
        self.app_ctx.push()

    def tearDown(self):
        self.app_ctx.pop()

    @patch("webapp.application._get_employee_directory_data")
    def test_populates_hiring_lead_and_interviews(self, mock_directory):
        """
        Ensure that _get_application populates
        hiring_lead data and scheduled interviews correctly
        """
        harvest = MagicMock(spec=Harvest)
        harvest.get_application.return_value = {
            "id": 123,
            "job_post_id": 10,
            "jobs": [{"id": 1, "name": "Original Role"}],
            "candidate_id": 55,
            "attachments": [],
            "current_stage": {"id": 999, "name": "Application Review"},
            "status": "active",
            "rejection_reason": {"type": {"id": 2}},
            "rejected_at": None,
        }
        harvest.get_job_post.return_value = {
            "job_id": 1,
            "title": "Original Role",
        }
        harvest.get_candidate.return_value = {
            "id": "cand-55",
            "email_addresses": [],
        }
        harvest.get_job.return_value = {
            "hiring_team": {
                "recruiters": [
                    {
                        "responsible": True,
                        "id": 88,
                        "employee_id": "1000",
                    }
                ]
            }
        }
        harvest.get_user.return_value = {
            "id": 88,
            "name": "Lead Name",
            "emails": "lead@example.com",
        }
        harvest.get_stages.return_value = [
            {
                "id": 999,
                "name": "Application Review",
                "interviews": [{"id": 1}],
            }
        ]
        harvest.get_interviews_scheduled.return_value = [
            {
                "status": "scheduled",
                "start": {"date_time": "2024-01-01T10:00:00+00:00"},
                "end": {"date_time": "2024-01-01T11:00:00+00:00"},
                "interview": {"id": 1, "name": "Initial call"},
                "interviewers": [
                    {"name": "Interviewer", "email": "int@example.com"}
                ],
                "external_event_id": "evt-1",
            }
        ]
        mock_directory.return_value = {
            "bio": "Line1\\nLine2",
            "name": "Lead Name",
            "avatar": "avatar.png",
            "id": "1000",
        }

        result = _get_application(harvest, "123")

        harvest.get_application.assert_called_once_with(123)
        harvest.get_job_post.assert_called_once_with(10)
        mock_directory.assert_called_once_with("1000")
        self.assertEqual(result["role_name"], "Original Role")
        self.assertEqual(result["hiring_lead"]["bio"], ["Line1", "Line2"])
        interview = result["scheduled_interviews"][0]
        self.assertEqual(interview["duration"], 60)
        self.assertEqual(interview["stage_name"], "Application Review")
        self.assertEqual(interview["interviewers"], [{"name": "Interviewer"}])


class TestGetApplicationFromToken(unittest.TestCase):
    def test_returns_application_for_valid_token(self):
        """
        Ensure that _get_application_from_token
        returns the application when given a valid token
        """
        harvest = MagicMock(spec=Harvest)
        mock_cipher = MagicMock()
        mock_cipher.decrypt.return_value = "123"

        with patch(
            "webapp.application._get_cipher", return_value=mock_cipher
        ), patch(
            "webapp.application._get_application", return_value={"id": 123}
        ) as mock_get_application:
            result = _get_application_from_token(harvest, "encrypted-token")

        mock_cipher.decrypt.assert_called_once_with("encrypted-token")
        mock_get_application.assert_called_once_with(harvest, "123")
        self.assertEqual(result, {"id": 123})

    def test_raises_invalid_token(self):
        """
        Ensure that _get_application_from_token
        raises InvalidToken when decryption fails
        """
        harvest = MagicMock(spec=Harvest)
        mock_cipher = MagicMock()
        mock_cipher.decrypt.side_effect = InvalidToken()

        with patch("webapp.application._get_cipher", return_value=mock_cipher):
            with self.assertRaises(InvalidToken):
                _get_application_from_token(harvest, "bad-token")


class TestSendMail(unittest.TestCase):
    @patch("webapp.application.SMTP")
    def test_send_mail_with_authentication(self, mock_smtp):
        """
        Ensure that _send_mail works correctly
        when SMTP authentication is required
        """
        smtp_instance = mock_smtp.return_value
        with patch.dict(
            os.environ,
            {
                "SMTP_SERVER": "smtp.example.com",
                "SMTP_USER": "user",
                "SMTP_PASS": "pass",
                "SMTP_SENDER_ADDRESS": "sender@example.com",
            },
            clear=True,
        ):
            _send_mail(
                to_email=["recipient@example.com"],
                subject="Subject",
                message="<p>Body</p>",
            )

        mock_smtp.assert_called_once_with(host="smtp.example.com")
        self.assertEqual(smtp_instance.ehlo.call_count, 2)
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with("user", "pass")
        smtp_instance.send_message.assert_called_once()
        smtp_instance.quit.assert_called_once()

    @patch("webapp.application.SMTP")
    def test_send_mail_without_authentication(self, mock_smtp):
        """
        Ensure that _send_mail works correctly
        when SMTP authentication is not required
        """
        smtp_instance = mock_smtp.return_value
        with patch.dict(
            os.environ,
            {
                "SMTP_SERVER": "smtp.example.com",
                "SMTP_USER": "",
                "SMTP_PASS": "",
                "SMTP_SENDER_ADDRESS": "sender@example.com",
            },
            clear=True,
        ):
            _send_mail(
                to_email=["recipient@example.com"],
                subject="Subject",
                message="<p>Body</p>",
            )

        mock_smtp.assert_called_once_with(host="smtp.example.com")
        smtp_instance.starttls.assert_not_called()
        smtp_instance.login.assert_not_called()
        smtp_instance.send_message.assert_called_once()
        smtp_instance.quit.assert_called_once()


class TestConfirmationToken(unittest.TestCase):
    @patch("webapp.application._get_cipher")
    def test_confirmation_token_encrypts_payload(self, mock_get_cipher):
        mock_cipher = MagicMock()
        mock_cipher.encrypt.return_value = "encrypted-token"
        mock_get_cipher.return_value = mock_cipher

        token = _confirmation_token(
            "candidate@example.com",
            "97001",
            "Accepted another offer",
            "12345",
        )

        expected_payload = json.dumps(
            {
                "email": "candidate@example.com",
                "withdrawal_reason_id": "97001",
                "withdrawal_message": "Accepted another offer",
                "application_id": "12345",
            }
        )
        mock_cipher.encrypt.assert_called_once_with(expected_payload)
        self.assertEqual(token, "encrypted-token")


class TestJobLocationCountries(unittest.TestCase):
    def setUp(self):
        self.patcher = patch(
            "webapp.application.REGION_COUNTRIES",
            {
                "emea": ["France", "Germany"],
                "apac": ["Japan"],
            },
        )
        self.mock_regions = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_returns_empty_for_non_remote_role(self):
        result = job_location_countries("Office Based - London, UK")
        self.assertEqual(result, [])

    def test_returns_countries_for_matching_region(self):
        result = job_location_countries("Home Based - EMEA")
        self.assertEqual(
            result,
            [
                {"@type": "Country", "name": "France"},
                {"@type": "Country", "name": "Germany"},
            ],
        )

    def test_worldwide_returns_all_regions(self):
        result = job_location_countries("Home based - Worldwide")
        self.assertEqual(
            result,
            [
                {"@type": "Country", "name": "France"},
                {"@type": "Country", "name": "Germany"},
                {"@type": "Country", "name": "Japan"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
