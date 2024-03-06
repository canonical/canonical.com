import unittest
from unittest.mock import MagicMock, patch
from webapp.google_calendar import CalendarAPI

# Interview calendar
INTERVIEW_CALENDAR = (
    "c_0a3348ba0132da2077be501edacc1ba7415ac132612d"
    + "264f99684232ee4ec491@group.calendar.google.com"
)


class TestGoogleCalendar(unittest.TestCase):
    @patch("webapp.google_calendar.build")
    @patch(
        "webapp.google_calendar.service_account."
        + "Credentials.from_service_account_info"
    )
    def setUp(self, mock_from_service_account_info, mock_build):
        # fake constants
        self.fake_calendar_id = "calendar_id"
        self.fake_event_id = "event_id"
        self.fake_timezone = "America/Toronto"
        self.fake_email = "email@email.com"

        # mock functions
        self.mock_service = MagicMock()
        self.mock_events = MagicMock()
        mock_from_service_account_info.return_value = MagicMock()

        # set return values of mocks
        self.mock_service.events.return_value = self.mock_events
        mock_build.return_value = self.mock_service

        # create a CalendarAPI object
        self.calendar_api = CalendarAPI()

    def test_delete_interview_event(self):
        # call the delete_interview_event method
        self.calendar_api.delete_interview_event(self.fake_event_id)

        # assertions
        self.mock_events.delete.assert_called_with(
            calendarId=INTERVIEW_CALENDAR,
            eventId=self.fake_event_id,
            sendUpdates="all",
        )
        self.mock_events.delete().execute.assert_called_once()

    def test_get_timezone(self):
        # create a mock_calendars object
        mock_calendars = MagicMock()

        # set return values
        self.mock_service.calendars.return_value = mock_calendars
        mock_calendars.get().execute.return_value = {
            "timeZone": self.fake_timezone
        }

        # call the get_timezone method
        timezone = self.calendar_api.get_timezone(self.fake_email)

        # assertions
        mock_calendars.get.assert_called_with(calendarId=self.fake_email)
        mock_calendars.get().execute.assert_called_once()
        self.assertEqual(timezone, self.fake_timezone)


if __name__ == "__main__":
    unittest.main()
