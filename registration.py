import hashlib
import sys
from sys import argv


from config.config import *
import sys
from sys import argv
from calendars.google_calendar_api import *
from volunteer.volunteer_slot import handle_volunteer
from volunteer.cancel_volunteer import handle_cancel_volunteer
from booking.make_booking import make_booking

def help_commands():

    #TO DO: REGISTRATION BEFORE EVERYTHING ELSE.

    commands =["VIEW_CALENDAR","MAKE_BOOKING","CANCEL_BOOKING","VOLUNTEER","CANCEL_VOLUNTEER" ]
    print(
    """
    LOGIN - register or log in

    VIEW CALENDAR - view upcoming events.

    MAKE BOOKING - Book a slot for code clinic session.

    CANCEL BOOKING - Cancel booked slot.

    VOLUNTEER - Volunteer for a code clinic session.

    CANCEL VOLUNTEER - Cancel volunteer slot.
    """)

    user_choice = input("what do you want to do?: ")
    if user_choice == commands[0].lower():
        view_students_calendar()
    # elif user_choice == commands[1].lower():
    #     make_booking()
    # elif user_choice == commands[2].lower():
    #     cancel_booking()
    # elif user_choice == commands[3].lower():
    #     handle_volunteer()
    # elif user_choice == commands[4].lower():
    #     handle_cancel_volunteer()   
    else:
        print("Sorry incorrect input.")



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_username_taken(username):
    try:
        with open("users_info.txt", "r") as file:
            for line in file:
                if line.startswith(f"Username: {username}"):
                    return True
    except FileNotFoundError:
        return False
    return False

def Register():
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        if is_username_taken(username):
            print("Username already taken. Please choose a different one.")
            continue

        password = input("Create password: ")
        confirm_password = input("Confirm password: ")

        if password == confirm_password:
            hashed_password = hash_password(confirm_password)
            with open("users_info.txt", "a") as user_info:
                user_info.write(f"Username: {username}\nPassword: {hashed_password}\n\n")
            print("Account has been created successfully!")
            break
        else:
            print("Error, passwords do not match.")

def Login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ")
    hashed_password = hash_password(password)
    
    try:
        with open("users_info.txt", "r") as file:
            users = file.read().split("\n\n")
            for user in users:
                if f"Username: {username}" in user and f"Password: {hashed_password}" in user:
                    print("Login successful!")
                    return True
        print("Error: Invalid username or password.")
        return False
    except FileNotFoundError:
        print("Error: No users found. Please register first.")
        return False

def main():


    print("""
          
        Welcome to coders clinic
          
        Please choose an option:
          
""")
    commands =["HELP","REGISTER", "LOGIN","VIEW_CALENDAR","MAKE_BOOKING","CANCEL_BOOKING","VOLUNTEER","CANCEL_VOLUNTEER" ]
    
    while True:
        choice = input("Do you want to register or login? (Register/Login): ").strip().lower()
        if choice == commands[1].lower():
            Register()
            user_input= input('Enter "help" to continue: ')
            if user_input == commands[0].lower():
                help_commands()
            break
        elif choice == commands[2].lower():
            Login()
            user_input= input('Enter "help" to continue: ')
            if user_input == commands[0].lower():
                help_commands()
                
            break
        else:
            print("Invalid choice. Please enter 'Register' to register or 'Login' to login.")


   
if __name__ == "__main__":
    main()









# commands =["HELP","LOGIN","VIEW_CALENDAR","MAKE_BOOKING","CANCEL_BOOKING","VOLUNTEER","CANCEL_VOLUNTEER" ]
#     if sys.argv[1] == commands[0].lower():
#         help_commands()
#     elif sys.argv[1] == commands[1].lower():
#         reg_or_login()
#         create_token()
#     elif sys.argv[1] == commands[2].lower():
#         view_students_calendar() 
#         view_code_clinics_calendar()
#     elif sys.argv[1] == commands[3].lower():
#         view_students_calendar() 
#         view_code_clinics_calendar()    
#         make_booking()
#     # elif sys.argv[1] == commands[4].lower():
#         view_students_calendar() 
#         view_code_clinics_calendar()
#         # cancel_booking()
#     elif sys.argv[1] == commands[5].lower():
#         view_students_calendar()
#         view_code_clinics_calendar()
#         handle_volunteer()
#     elif sys.argv[1] == commands[6].lower():
#         view_students_calendar()
#         view_code_clinics_calendar()
#         handle_cancel_volunteer()

#     fetch_clinic_calendar_events()
