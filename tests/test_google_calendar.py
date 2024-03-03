import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
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

    def test_get_events(self):
        # create datetime objects for start and end
        start = datetime.now() - timedelta(days=1)
        end = datetime.now()

        # call the get_events method
        self.calendar_api.get_events(self.fake_calendar_id, start, end)

        # assertions
        self.mock_events.list.assert_called_with(
            calendarId=self.fake_calendar_id,
            timeMin=start.isoformat() + "Z",
            timeMax=end.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        self.mock_events.list().execute.assert_called_once()

    def test_get_single_event(self):
        # call the get_single_event method
        self.calendar_api.get_single_event(
            self.fake_calendar_id, self.fake_event_id
        )

        # assertions
        self.mock_events.get.assert_called_with(
            calendarId=self.fake_calendar_id,
            eventId=self.fake_event_id,
        )
        self.mock_events.get().execute.assert_called_once()

    def test_delete_event(self):
        # call the delete_event method
        self.calendar_api.delete_event(
            self.fake_calendar_id, self.fake_event_id
        )

        # assertions
        self.mock_events.delete.assert_called_with(
            calendarId=self.fake_calendar_id,
            eventId=self.fake_event_id,
            sendUpdates="all",
        )
        self.mock_events.delete().execute.assert_called_once()

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
