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

def create_calendar_if_not_exists(service):
    try:
        calendar_id = get_calendar_id(service)
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

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def add_volunteer_event(service, calendar_id, volunteer_info):
    event = {
        'summary': f'Volunteer Availability - {volunteer_info["email"]}',
        'location': volunteer_info['campus'],
        'description': f'Volunteer available at {volunteer_info["campus"]}, email: {volunteer_info["email"]}',
        'start': {
            'dateTime': volunteer_info['start_time'],
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': volunteer_info['end_time'],
            'timeZone': 'Africa/Johannesburg',
        },
        'attendees': [
            {'email': volunteer_info['email']},
        ],
    }
    
    try:
        event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    creds = create_token()
    service = build('calendar', 'v3', credentials=creds)

    # Ensure the Coders-Clinic calendar exists
    calendar_id = create_calendar_if_not_exists(service)
    if not calendar_id:
        print("Failed to create or find the Coders-Clinic calendar.")
        return

    # Gather volunteer information
    email = input("Enter your email: ")
    campus = input("Enter your campus location: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    start_time = input("Enter the start time (HH:MM, 24-hour format): ")
    end_time = input("Enter the end time (HH:MM, 24-hour format): ")

    # Format the start and end time for the event
    start_datetime = f"{start_date}T{start_time}:00"
    end_datetime = f"{start_date}T{end_time}:00"

    # Create volunteer info dictionary
    volunteer_info = {
        "email": email,
        "campus": campus,
        "start_time": start_datetime,
        "end_time": end_datetime
    }

    # Add volunteer event to the Coders-Clinic calendar
    add_volunteer_event(service, calendar_id, volunteer_info)

if __name__ == '__main__':
    main()
