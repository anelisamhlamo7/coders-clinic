from config.config import *
import sys
from sys import argv
from calendars.google_calendar_api import *
from volunteer.volunteer_slot import handle_volunteer
from volunteer.cancel_volunteer import handle_cancel_volunteer
from booking.make_booking import make_booking


def help_Command():
    print("HELP - Provides information on commands.\nLOGIN - will prompt you to register or login. \nVIEW CALENDAR - shows upcoming events.\nMAKE BOOKING - Books a slot for code clinics.\nCANCEL BOOKING - Cancels booked slot.\nVOLUNTEER - Volunteer for a code clinic session.\nCANCEL VOLUNTEER - Cancels volunteer slot.")

    """
    HELP - Provides information on commands.
    LOGIN - registers or logs you in
    VIEW CALENDAR - shows upcoming events.
    MAKE BOOKING - Books a slot for code clinic session.
    CANCEL BOOKING - Cancels booked slot.
    VOLUNTEER - Volunteer for a code clinic session.
    CANCEL VOLUNTEER - Cancels volunteer slot.
    """

def main():

    commands =["HELP","LOGIN","VIEW_CALENDAR","MAKE_BOOKING","CANCEL_BOOKING","VOLUNTEER","CANCEL_VOLUNTEER" ]
    if sys.argv[1] == commands[0].lower():
        help_Command()
    elif sys.argv[1] == commands[1].lower():
        reg_or_login()
        create_token()
    elif sys.argv[1] == commands[2].lower():
        view_students_calendar() 
        view_code_clinics_calendar()
    elif sys.argv[1] == commands[3].lower():
        view_students_calendar() 
        view_code_clinics_calendar()    
        make_booking()
    # elif sys.argv[1] == commands[4].lower():
        view_students_calendar() 
        view_code_clinics_calendar()
        # cancel_booking()
    elif sys.argv[1] == commands[5].lower():
        view_students_calendar()
        view_code_clinics_calendar()
        handle_volunteer()
    elif sys.argv[1] == commands[6].lower():
        view_students_calendar()
        view_code_clinics_calendar()
        handle_cancel_volunteer()

    fetch_clinic_calendar_events()

        



if __name__ == "__main__":
    # fetch_clinic_calendar_events()
    main()

