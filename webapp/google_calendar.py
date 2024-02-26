from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

# Google Calendar credentials
SERVICE_ACCOUNT_INFO = {
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_email": os.environ.get("SERVICE_ACCOUNT_EMAIL"),
    "private_key": os.environ.get("SERVICE_ACCOUNT_PRIVATE_KEY").replace("\\n", "\n"),
}

# Workplace Engineering account
WPE_EMAIL = "wpe-data@canonical.com"

# Interview calendar
INTERVIEW_CALENDAR = "c_0a3348ba0132da2077be501edacc1ba7415ac132612d264f99684232ee4ec491@group.calendar.google.com"

class CalendarAPI:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_INFO, scopes=SCOPES
        )
        try:
            delegated_credentials = credentials.with_subject(WPE_EMAIL)
            service = build(
                "calendar", "v3", credentials=delegated_credentials
            )
        except HttpError as error:
            print("An error occurred: %s" % error)

        return service
    
    def get_events(self, calendar_id, start, end):
        return (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start.isoformat() + "Z",
                timeMax=end.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    
    def get_single_event(self, calendar_id, event_id):
        return (
            self.service.events()
            .get(
                calendarId=calendar_id,
                eventId=event_id
            )
            .execute()
        )
    
    def delete_event(self, calendar_id, event_id):
        return (
            self.service.events()
            .delete(
                calendarId=calendar_id,
                eventId=event_id,
                sendUpdates="all"
            )
            .execute()
        )
    
    def delete_event_from_interview_calendar(self, event_id):
        return (
            self.service.events()
            .delete(
                calendarId=INTERVIEW_CALENDAR,
                eventId=event_id,
                sendUpdates="all"
            )
            .execute()
        )
    
    def get_timezone(self, email):
        calendar = self.service.calendars().get(calendarId=email).execute()

        return calendar["timeZone"]