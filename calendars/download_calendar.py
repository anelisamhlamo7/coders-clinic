from config.config import *

def make_calendar():
    creds = create_token()

    service = build("calendar","v3" , credentials = creds)

    calendar = {
        "summary": "Code_clinic_21",
        "timeZone": "Africa/Johannesburg" 
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar["id"]


