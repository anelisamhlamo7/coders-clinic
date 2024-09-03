from rich.console import Console
from rich.table import Table
import json
from config.config import *
import datetime

def fetch_clinic_calendar_events():
    try:
        calendar_ID = "c_135c6a1b34b9ad1506550f6948e7a9265bae8eecfb914326a0b3c9301f67cd6e@group.calendar.google.com"
        service = build("calendar", "v3", credentials=create_token())
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
        service.events()
        .list(
            calendarId=calendar_ID,
            timeMin=now,
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events found.")
            return
        
        with open("events_data.json", "w") as data:
            json.dump(events,data,indent=4)

        
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    return events
  

def view_code_clinics_calendar():
    console = Console()
    table = Table(title="Code Clinics Calendar")

    today = datetime.datetime.now().date()
    table.add_column("TIME", justify="center")

    date_columns = [today + datetime.timedelta(days=i) for i in range(8)]
    for date in date_columns:
        table.add_column(str(date), justify="center")

    table.add_column("Attendees",justify="center")

    


    time_slots = [(hour, minute) for hour in range(9, 17) for minute in [0, 30]]

    events = {date: {f"{hour:02d}:{minute:02d}": [] for hour, minute in time_slots} for date in date_columns}
    google_calendar_events = fetch_clinic_calendar_events()

    for event in google_calendar_events:
        start_datetime = datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")
        date = start_datetime.date()
        time_slot = start_datetime.strftime('%H:%M')
        events[date][time_slot].append(event['summary'])
        


    # Add the time slots as rows
    for hour, minute in time_slots:
        time_slot_label = f"{hour:02d}:{minute:02d}"
        row_data = []
        for date in date_columns:
            # attendees = event['attendees'][0]['email']
            event_summaries = events[date][time_slot_label]
            if event_summaries:
                row_data.append("\n".join(event_summaries))
                # row_data.append(attendees)
            else:
                row_data.append("")
        table.add_row(time_slot_label, *row_data)

    # Print the table
    console.print(table)


def fetch_student_calendar_events():
    try:
        calendar_ID = "primary"
        service = build("calendar", "v3", credentials=create_token())
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
        service.events()
        .list(
            calendarId=calendar_ID,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    return events

def view_students_calendar():
    console = Console()
    table = Table(title="Student Calendar")

    today = datetime.datetime.now().date()
    table.add_column("TIME", justify="center")

    date_columns = [today + datetime.timedelta(days=i) for i in range(8)]
    for date in date_columns:
        table.add_column(str(date), justify="center")

    # Retrieve events from Google Calendar
    google_calendar_events = fetch_student_calendar_events()

    # Collect start times of events
    event_start_times = []
    for event in google_calendar_events:
        start_datetime = datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")
        event_start_times.append(start_datetime.time())

    # Sort and remove duplicates from the event start times
    event_start_times = sorted(set(event_start_times))

    # Add the event start times as rows
    for start_time in event_start_times:
        time_slot_label = start_time.strftime('%H:%M')
        row_data = []
        for date in date_columns:
            events_on_date = [event for event in google_calendar_events if
                              datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z").date() == date]
            event_summaries = [event['summary'] for event in events_on_date if
                               datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z").time() == start_time]
            if event_summaries:
                row_data.append("\n".join(event_summaries))
            else:
                row_data.append("")
        table.add_row(time_slot_label, *row_data)

    # Print the table
    console.print(table)
