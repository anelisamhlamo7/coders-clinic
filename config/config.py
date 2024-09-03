import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_token():

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

  # print("Connection to google calendar succesful!")
  return creds

def hidden_config():


  path = os.path.expanduser("~") +f"/.configuration"
  os.mkdir(path)
  

def Register():
  while True:
    username = input("Enter username: ")
    password = input("Create password: ")
    confirm_password = input("Confirm password: ")

    if password == confirm_password:
      user_info = open("users_info.txt","a") 
      user_info.write(f"Username: {username}\nPassword: {confirm_password}")
      user_info.close()
      print("Account has been created successfully!")
      break
    elif password != confirm_password:
      print("Error, passwords do not match.")
      continue

def login():
  while True:
    username = input("Enter username: ")
    password = input("Enter password: ")

    user_info = open("users_info.txt","r").read()

    if username and password in user_info:
      print("Login successful!")
      break
    else:
      print("Invalid username or password.")
      continue


def reg_or_login():
  while True:
    reg_or_login = input("Would you like to register or login? ")

    if reg_or_login == "register":
      Register()
    elif reg_or_login == "login":
      login()
      break
    else:
      print("Sorry incorrect input.")

