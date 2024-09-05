from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import os.path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_token():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_id(service):
    calendars = service.calendarList().list().execute()
    for calendar in calendars.get('items', []):
        if calendar.get('summary') == 'Coders-Clinic':
            return calendar['id']
    return None

def list_volunteer_events(service, calendar_id, email):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    volunteer_events = [event for event in events if event.get('attendees') and
                        any(attendee['email'] == email for attendee in event['attendees'])]

    if not volunteer_events:
        print("No upcoming events found for your email.")
        return []

    print(f"Upcoming events for {email}:")
    for idx, event in enumerate(volunteer_events, 1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{idx}. {event['summary']} - {start} (Event ID: {event['id']})")
    return volunteer_events

def cancel_volunteer_event(service, calendar_id, event_id):
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        print(f"Event {event_id} has been successfully canceled.")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    creds = create_token()
    service = build('calendar', 'v3', credentials=creds)

    # Ensure the Coders-Clinic calendar exists
    calendar_id = get_calendar_id(service)
    if not calendar_id:
        print("Coders-Clinic calendar not found.")
        return

    # Gather volunteer email to find events
    email = input("Enter your email to find your events: ")
    events = list_volunteer_events(service, calendar_id, email)

    if events:
        # Prompt the volunteer to select the event to cancel
        event_number = int(input("Enter the number of the event to cancel (or 0 to exit): "))
        if event_number > 0 and event_number <= len(events):
            event_id = events[event_number - 1]['id']
            cancel_volunteer_event(service, calendar_id, event_id)
        else:
            print("Invalid selection, exiting.")

if __name__ == '__main__':
    main()
