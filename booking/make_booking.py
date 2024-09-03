import datetime as dt
import os.path
from config.config import *

SCOPES = ["https://www.googleapis.com/auth/calendar"]

volunteered_slots = []
def main():
    # Check if token.json exists and load credentials from it
    creds = create_token()
    try:
        # Build the service object for the Google Calendar API
        service = build("calendar", "v3", credentials=creds)

        # Get the current date and time in UTC
        now = dt.datetime.utcnow().isoformat() + 'Z'

        # Calculate the end date as 7 days from now
        end_date = (dt.datetime.utcnow() + dt.timedelta(days=7)).isoformat() + 'Z'

        # Call the Google Calendar API to retrieve events within the next 7 days
        event_results = service.events().list(
            calendarId="c_135c6a1b34b9ad1506550f6948e7a9265bae8eecfb914326a0b3c9301f67cd6e@group.calendar.google.com",
            timeMin=now,
            timeMax=end_date,
            maxResults=7,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        # Extract the events from the API response
        events = event_results.get("items", [])

        # If no events are found, print a message and return
        if not events:
            print("No upcoming events found!")
            return

        # Initialize a list to store the upcoming events
        

        # Iterate over the events and print the start time and summary
        for event in events:
            start = event['start'].get('dateTime', event['start'].get("date"))
            volunteered_slots.append(f'{start} {event["summary"]}')
            print(start, event["summary"])

        # Return the list of upcoming events
        return volunteered_slots

    except HttpError as error:
        # Handle HTTP errors
        print(f"An error occurred: {error}")



def add_event(date_input, time_input, x):
  creds = create_token()

  try:

    #ask users what they are booking for 
    Booking_description = input("What do you need help with? ")

    #allows you to edit event
    service = build("calendar", "v3", credentials=creds)

    event = {
    'summary': 'Code Clinics Session',
    'location': 'WeThinkCode_',
    'description': f'{Booking_description}',
    'colorId': 6,
    'start': {
        'dateTime': date_input + 'T' + time_input + ':00+02:00',
        'timeZone': 'Europe/Vienna'
    },
    'end': {
        'dateTime': date_input + 'T' + time_input[:3] + '30' + ':00+02:00',
        'timeZone': 'Europe/Vienna'
    },
    'attendees': [
        {'email': 'afunda023@student.wethinkcode.co.za'},
        {'email': 'afrikafunda@gmail.com'}
    ]
}
                               
    #event = service.events().insert(calendarId='c_5a20a2d16d037119888fba82a6d3f43aaa0015acbffabfea0f62db268c64a03b@group.calendar.google.com', body=event).execute()

    created_event = service.events().insert(calendarId='c_5a20a2d16d037119888fba82a6d3f43aaa0015acbffabfea0f62db268c64a03b@group.calendar.google.com', body=event).execute()

    # Extract the event ID from the created event
    event_id = created_event['id']
    print(f"Event created with ID: {event_id}")

    # Store the event ID in a list or database for future reference
    # You can create a list or use a database to store multiple event IDs
    event_ids = []
    event_ids.append(event_id)
    bookedslot_event_id.update({x:event_id})
    print(bookedslot_event_id)


    print(f"Event created {created_event.get('htmlLink')}")

  except HttpError as error:
    print(f"An error occurred: {error}")
    
booked = {}
bookedslot_event_id = {}

def available_slots():
  
  print("Hi Welcome to Code Clinics")
  print("As Seen On The Calender, Your Available slots are:")
#   for event in volunteered_slots:
#     print(f"> {event}")

  #add condition to check if 2024-02-04 is digits and 
  print("Please Select The Date You Would like to Book For(Use the 'yyyy-mm-dd')?")
#   print("Available Dates:")

  #PRINT OUT AVAILABLE DATES
  available_dates = []
  for i in volunteered_slots:
    date = i.split('T',)[0]
    if date not in available_dates:
      available_dates.append(date)
      print(f'{date}')

  #PROMPT USER TO CHOOSE FROM DATES SUPPLIED
  while True:
      date_input = input("Choose From Dates Supplied: ").lower()
      if len(date_input) == 10 and (date_input[:4].isdigit() and date_input[5:7].isdigit() and date_input[-2:].isdigit()) and date_input[4:5] == "-"  and date_input[7:8] == "-" :
          # print('yes')
          if date_input not in available_dates:
              print('Please Choose From Available Alots')
          else:
              break
      else:
          print('Please Enter Date in YYYY-MM-DD Format')

  #PRINT TIMES AVAILABLE
  date_times_dict = {date_input:[]}

  print(f"Here Are The Time Slots Available On: {date_input}")
  for slot in volunteered_slots:
      if date_input == slot.split('T')[0]:
          time_available = slot.split("T")[1][:5]
          date_times_dict[date_input].append(time_available)
          if slot.endswith( " (Booked)"):
             print(f'> {time_available} (Booked)')
          else:
             #date_times_dict[date_input].append(time_available)
             print(f'> {time_available}')
           
          
  #PROMPT USER TO SELECT FROM AVAILABLE TIMES
  # print(date_times_dict)
#   print(booked)
  while True:
    time_input = input("Please Choose Time From The Available Time Slots: ").lower()
    if booked:
        booked.update({date_input:[]})
        booked[date_input].append(time_input)
        if time_input in date_times_dict[date_input] and time_input not in booked[date_input] :
              booked[date_input].append(time_input)
              print('Time Selected')
              break
        elif time_input in date_times_dict[date_input] and time_input in booked[date_input]:
              print('Slot Already Booked!')
        else:
              print('The Selected Time Slot is Unavailable')
    else:
        booked.update({date_input:[]})
        booked[date_input].append(time_input)
        if time_input in date_times_dict[date_input]:
              print('Time Selected')
              break
        else:
              print('The Selected Time Slot is Unavailable')
       


#   print(date_times_dict)
#   print(booked)
  #marks slot as booking if it is
  for i in range(len(volunteered_slots)):
     if date_input in volunteered_slots[i] and time_input in volunteered_slots[i]:
        volunteered_slots[i] += " (Booked)"
        print(volunteered_slots[i])
        bookedslot_event_id.update({volunteered_slots[i]:''})
        add_event(date_input,time_input, volunteered_slots[i])

def delete_event():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      

      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  #bookedslot_event_id {} = { 'booked slot': 'sdfghjklm', 'booked slot': 'sdfghjklm'}
  
  while True:
    booking_to_cancel = input('What do you want to cancel? ')
    for i in bookedslot_event_id.keys():
        print(i)
    if booking_to_cancel in bookedslot_event_id:
        canceled_value = bookedslot_event_id[booking_to_cancel]
        print(f"The value for {booking_to_cancel} is: {canceled_value}")
        # Add any additional logic you need here
        break  # Exiting the loop assuming one cancellation at a time
    else:
        print(f"{booking_to_cancel} not found. Please enter a valid booking.")

  try:

    service = build("calendar", "v3", credentials=creds)
    # Assuming 'service' is your Calendar API service instance
    service.events().delete(calendarId="c_135c6a1b34b9ad1506550f6948e7a9265bae8eecfb914326a0b3c9301f67cd6e@group.calendar.google.com", eventId=canceled_value).execute()
    print(f"Event with ID {canceled_value} deleted successfully.")
    
  except HttpError as error:
    print(f"An error occurred: {error}")

def make_booking():
    main()
    
    available_slots()
  

if __name__ == "__main__":
  #you will most likely have to most your lists outside the functions
  main()
  for i in range(3):
    available_slots()