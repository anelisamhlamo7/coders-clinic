from datetime import datetime ,timedelta
from config.config import *
import json
from json import JSONDecodeError

def create_volunteer_slot(event_time, attendee_email, event_description):

    event = {
        'summary': 'Volunteer',
        'location': '331 Albert RdWoodstock, Cape Town, 7915',
        'description': event_description,
        'start': {
            'dateTime': event_time.isoformat(),
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': (event_time + timedelta(minutes=30)).isoformat(),
            'timeZone': 'Africa/Johannesburg',
        },
        'attendees': [
            {'email': attendee_email}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    creds = create_token()
    service = build("calendar", "v3", credentials=creds)

    event = service.events().insert(calendarId="c_135c6a1b34b9ad1506550f6948e7a9265bae8eecfb914326a0b3c9301f67cd6e@group.calendar.google.com", body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def add_event(event_time, attendee_email):
    print(f"'{attendee_email}' booked as Volunteer for {event_time}")

def get_volunteer_booking_info():
    print("Please provide the following details to book as a volunteer:")
    while True:
        event_date= input("Enter the date for the booking (e.g., 2024-02-22): ")
        event_time = input("Enter the time you would like to volunteer for (e.g.,12:00): ")

        date_time = (f"{event_date} {event_time}")
        if is_valid_datetime(date_time):
            valid_datetime = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        else:
            print("Invalid date format or invalid time format. Please try again.")
            continue

        event_description = input("Enter event description: ")
        attendee_email= input("Enter your student email: ")
        return {
            'date_time':valid_datetime,
            'event_description': event_description,
            'attendee_email': attendee_email
        }
    
def check_double_book(event_time):
    event_time = event_time.isoformat() + "+02:00"

    try:

        with open("events_data.json", "r") as data:

            events = json.load(data)

            for event in events:
                if event_time == event['start']['dateTime']:
                    print("Volunteer already booked. Choose another time.") 

                    return False

            return True
    except JSONDecodeError as Error:
        print("Events empty")
        return True

            
def handle_volunteer():
    while True:
        volunteer_info = get_volunteer_booking_info()
        event_time = volunteer_info["date_time"]
        attendee_email = volunteer_info["attendee_email"]
        event_description = volunteer_info['event_description']
        if check_double_book(event_time):
            create_volunteer_slot(event_time,attendee_email,event_description)
            add_event(event_time, event_description)
            break
        

def is_valid_datetime(date_time)->bool:
    try:
        datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
