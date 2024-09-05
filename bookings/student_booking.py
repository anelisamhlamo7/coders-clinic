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

def get_calendar_id(service, summary):
    calendars = service.calendarList().list().execute()
    for calendar in calendars.get('items', []):
        if calendar.get('summary') == summary:
            return calendar['id']
    return None

def list_available_volunteer_slots(service, calendar_id):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    available_slots = [event for event in events if "Volunteer Availability" in event['summary'] and not "Student Booking" in event['summary']]

    if not available_slots:
        print("No available volunteer slots found.")
        return []

    print("Available volunteer slots:")
    for idx, event in enumerate(available_slots, 1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{idx}. {event['summary']} - {start} (Event ID: {event['id']})")
    return available_slots

def book_slot(service, calendar_id, volunteer_event, student_info):
    volunteer_email = volunteer_event['attendees'][0]['email']
    
    # Update volunteer calendar with the student booking
    updated_volunteer_event = {
        'summary': f'Booked by {student_info["email"]}',
        'description': f'{student_info["help_description"]}',
        'start': volunteer_event['start'],
        'end': volunteer_event['end'],
        'attendees': [
            {'email': student_info['email']},
            {'email': volunteer_email}
        ],
    }

    try:
        service.events().update(calendarId=calendar_id, eventId=volunteer_event['id'], body=updated_volunteer_event).execute()
        print(f"Booking updated in volunteer's calendar.")
    except HttpError as error:
        print(f"An error occurred while updating volunteer calendar: {error}")
        return

    # Update student calendar with the booked slot
    student_calendar_id = get_calendar_id(service, f"{student_info['email']}'s Calendar")
    if not student_calendar_id:
        print("Student calendar not found.")
        return

    student_event = {
        'summary': f'Booked slot with Volunteer {volunteer_email}',
        'description': f'{student_info["help_description"]}',
        'start': volunteer_event['start'],
        'end': volunteer_event['end'],
        'attendees': [
            {'email': student_info['email']},
            {'email': volunteer_email}
        ],
    }

    try:
        service.events().insert(calendarId=student_calendar_id, body=student_event).execute()
        print(f"Event added to student calendar.")
    except HttpError as error:
        print(f"An error occurred while adding to student calendar: {error}")

def main():
    creds = create_token()
    service = build('calendar', 'v3', credentials=creds)

    # Get the Coders-Clinic calendar ID
    calendar_id = get_calendar_id(service, 'Coders-Clinic')
    if not calendar_id:
        print("Coders-Clinic calendar not found.")
        return

    # List available volunteer slots
    available_slots = list_available_volunteer_slots(service, calendar_id)
    if not available_slots:
        return

    # Ask student to select a slot
    slot_number = int(input("Enter the number of the slot you want to book (or 0 to exit): "))
    if slot_number < 1 or slot_number > len(available_slots):
        print("Invalid selection, exiting.")
        return

    volunteer_event = available_slots[slot_number - 1]

    # Gather student information
    student_email = input("Enter your email: ")
    student_help_description = input("Describe the help you need: ")

    student_info = {
        "email": student_email,
        "help_description": student_help_description
    }

    # Book the slot
    book_slot(service, calendar_id, volunteer_event, student_info)

if __name__ == '__main__':
    main()
