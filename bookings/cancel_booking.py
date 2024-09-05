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

def list_student_bookings(service, student_email):
    student_calendar_id = get_calendar_id(service, f"{student_email}'s Calendar")
    if not student_calendar_id:
        print("Student calendar not found.")
        return []

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId=student_calendar_id, timeMin=now,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    bookings = [event for event in events if "Booked slot with Volunteer" in event['summary']]
    
    if not bookings:
        print("No bookings found.")
        return []

    print("Your bookings:")
    for idx, event in enumerate(bookings, 1):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{idx}. {event['summary']} - {start} (Event ID: {event['id']})")
    return bookings

def cancel_booking(service, student_email, booking_event_id):
    student_calendar_id = get_calendar_id(service, f"{student_email}'s Calendar")
    if not student_calendar_id:
        print("Student calendar not found.")
        return

    try:
        service.events().delete(calendarId=student_calendar_id, eventId=booking_event_id).execute()
        print("Booking removed from student calendar.")
    except HttpError as error:
        print(f"An error occurred while removing from student calendar: {error}")
        return

    # Get volunteer email from the event to update the volunteer's calendar
    event = service.events().get(calendarId=student_calendar_id, eventId=booking_event_id).execute()
    volunteer_email = [
            attendee['email'] for attendee in event.get('attendees', []) if attendee['email'] != student_email]

    if not volunteer_email:
        print("Volunteer email not found.")
        return

    volunteer_calendar_id = get_calendar_id(service, f"{volunteer_email[0]}'s Calendar")
    if not volunteer_calendar_id:
        print("Volunteer calendar not found.")
        return

    try:
        service.events().delete(calendarId=volunteer_calendar_id, eventId=booking_event_id).execute()
        print("Booking removed from volunteer calendar.")
    except HttpError as error:
        print(f"An error occurred while removing from volunteer calendar: {error}")

def main():
    creds = create_token()
    service = build('calendar', 'v3', credentials=creds)
    
    student_email = input("Enter your email: ").strip()
    
    # List bookings and let the student select one to cancel
    bookings = list_student_bookings(service, student_email)
    if not bookings:
        return

    try:
        booking_index = int(input("Enter the number of the booking you want to cancel: ")) - 1
        if booking_index < 0 or booking_index >= len(bookings):
            print("Invalid selection.")
            return
        booking_event_id = bookings[booking_index]['id']
        cancel_booking(service, student_email, booking_event_id)
    except ValueError:
        print("Invalid input.")

if __name__ == '__main__':
    main()

