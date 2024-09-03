from booking.make_booking import *
from config.config import *


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def delete_event():
  creds = create_token()

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
