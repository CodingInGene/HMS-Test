import requests

# For google calender
import os
import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Serverless email sending
def send_email(purpose, recipient_email, recipient_name, body):
    try:
        endpoint = "http://localhost:3000/sendmail/"

        headers = {"Content-Type": "application/json"}

        # Purpose - signup/appointment
        data = {
            "purpose": purpose,
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "email_body": body
        }

        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Email service error: {e}")
        return False


# Google calender events creation
def create_event(doctor_name, patient_name, doctor_email, patient_email, start_time, end_time):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    token_path = os.path.join(BASE_DIR, "token.json")
    creds_path = os.path.join(BASE_DIR, "client_secret_hmsAvoy.calender-api.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=8888, prompt="select_account")
        
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        today = datetime.today().strftime("%Y-%m-%d")

        print(f"start: {today}T{start_time}")
        print(f"end: {today}T{end_time}")
        print(f"doctor_email: {doctor_email}")
        print(f"patient_email: {patient_email}")

        # Create the event
        event = {
            "summary": f"Appointment: {patient_name} with Dr. {doctor_name}",
            "description": f"Medical appointment between {patient_name} and Dr. {doctor_name}",
            "start": {
                "dateTime": f"{today}T{start_time}",    # yyyy-mm-ddThh:MM:ss
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": f"{today}T{end_time}",
                "timeZone": "Asia/Kolkata",
            },
            # Invite doctor and patient as attendees
            "attendees": [
                {"email": doctor_email},
                {"email": patient_email},
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 60},
                    {"method": "popup", "minutes": 30},
                ],
            },
        }

        event = service.events().insert(
            calendarId="primary",
            body=event,
            sendUpdates="all"  # sends email invite to attendees
        ).execute()

        print(f"Event created: {event.get('htmlLink')}")
        return event

    except HttpError as error:
        print(f"An error occurred: {error}")
        return