
from urllib.error import HTTPError
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

import os.path


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_token():
    creds = None
    # Check if token.json exists (contains previously saved credentials)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If credentials are not available or invalid, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_id(service):

    calendars = service.calendarList().list().execute()
    
    # Iterate through each calendar
    for calendar in calendars.get('items', []):
        if calendar.get('summary') == 'Coders-Clinic':
            return calendar['id']
    
    # If the calendar is not found, return None
    return None



def create_calendar_if_not_exists(service):
    try:
        # Get the calendar ID of the Coders-Clinic calendar
        calendar_id = get_calendar_id(service)
        
        # If the Coders-Clinic calendar doesn't exist, create a new one
        if calendar_id is None:
            print("Coders-Clinic calendar not found. Creating a new one...")
            calendar = {
                'summary': 'Coders-Clinic',
                'timeZone': 'Africa/Johannesburg'
            }
            created_calendar = service.calendars().insert(body=calendar).execute()
            calendar_id = created_calendar['id']
            print(f"New Coders-Clinic calendar created with ID: {calendar_id}")
        else:
            print(f"Coders-Clinic calendar already exists with ID: {calendar_id}")

        return calendar_id

    except HTTPError as error:
        print(f"An error occurred: {error}")
        return None

def main():
    creds = create_token()
    service = build('calendar', 'v3', credentials=creds)

    # Ensure the Coders-Clinic calendar exists (create if necessary)
    calendar_id = create_calendar_if_not_exists(service)
    if not calendar_id:
        print("Failed to create or find the Coders-Clinic calendar.")
        return

    # Get the next 10 upcoming events from the Coders-Clinic calendar
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()


