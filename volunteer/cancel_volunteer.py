from datetime import datetime
from config.config import *
import json

def cancel_volunteer_slot(event_id):
    creds = create_token()
    service = build("calendar","v3",credentials=creds)
    service.events().delete(calendarId="c_135c6a1b34b9ad1506550f6948e7a9265bae8eecfb914326a0b3c9301f67cd6e@group.calendar.google.com", eventId=event_id).execute()

    remove_event_data(event_id)

def check_volunteer_book(event_time,attendee_email):
    event_time = event_time.isoformat()+ "+02:00"

    with open("events_data.json", "r") as data:

        events = json.load(data)

        for event in events:
            if event['summary'] == "Volunteer" and attendee_email == event['attendees'][0]['email'] and event_time == event['start']['dateTime'] :

                return event['id']
            
        else:
            print("Cannot cancel a non-existent event.")
            return None
                
    
    
def remove_event(event_description,attendee_email):
    print(f"Booked '{event_description}' canceled for {attendee_email}")

def get_volunteer_booking_info():
    print("Please provide the following details to cancel your volunteer slot:")
    while True:
        event_date= input("Enter the date you chose to volunteer (e.g., 2024-02-22): ")
        event_time = input("Enter the time you would like to cancel (e.g.,12:00): ")
        date_time = (f"{event_date} {event_time}")
        if is_valid_datetime(date_time):
            date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M")  # Convert input string to datetime object
        else:
            print("Invalid date format or invalid time format. Please try again.")
            continue

        attendee_email= input("Enter your student email: ")
        return {
            'date_time': date_time,
            'attendee_email': attendee_email
        }
def remove_event_data(event_id):

    with open("events_data.json", "r") as data:
        events = json.load(data)

        for event in events:
            if event_id == event['id']:
                events.remove(event)

 


def handle_cancel_volunteer():
    volunteer_info = get_volunteer_booking_info()
    event_time = volunteer_info['date_time']
    attendee_email = volunteer_info['attendee_email']
    event_description = "Volunteer slot"

    if check_volunteer_book(event_time,attendee_email) != None:
        event_id = check_volunteer_book(event_time,attendee_email)
        cancel_volunteer_slot(event_id)
        remove_event(event_description,attendee_email)



def is_valid_datetime(date_time)->bool:
    try:
        datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
