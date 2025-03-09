import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

SERVICE_ACCOUNT_FILE = "service_account_credentials.json"

CALENDAR_ID = "sthor726@gmail.com"  

def getCalendarEvents(number_of_events=5):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        service = build("calendar", "v3", credentials=credentials)

        now = datetime.datetime.utcnow().isoformat() + "Z"

        print("Fetching the nearest upcoming events...")

        
        events_result = (
            service.events()
            .list(
                calendarId=CALENDAR_ID,
                timeMin=now, 
                maxResults=number_of_events,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        nearest_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            nearest_events.append({"start": start, "summary": event["summary"]})

        return nearest_events

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

if __name__ == "__main__":
    upcoming_events = getCalendarEvents(5)
    for event in upcoming_events:
        print(f"{event['start']} - {event['summary']}")
