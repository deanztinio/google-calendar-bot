from datetime import datetime, timedelta
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define scopes and token path
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pkl'

# Your actual credentials from Google Cloud
CREDENTIALS = {
    "installed": {
        "client_id": "1023408752441-osic1fbv1vb185sjo1jfjt74m12kasjq.apps.googleusercontent.com",
        "client_secret": "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",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

# Initialize Google Calendar service
def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_config(CREDENTIALS, SCOPES)
        creds = flow.run_console()
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

# Check if event exists already to avoid duplicates
def event_exists(service, calendar_id, summary, start_time):
    time_min = start_time.isoformat()
    time_max = (start_time + timedelta(minutes=1)).isoformat()

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        q=summary,
        singleEvents=True
    ).execute()

    for event in events_result.get('items', []):
        if summary in event.get('summary', '') and 'created_by_calendar_bot' in event.get('description', ''):
            return True
    return False

# Safely create an event
def create_training_event(summary, description, start_time, duration_minutes=60):
    service = get_calendar_service()
    calendar_id = 'primary'

    if event_exists(service, calendar_id, summary, start_time):
        print(f"⚠️ Event '{summary}' already exists at {start_time}. Skipping.")
        return

    event = {
        'summary': summary,
        'description': f"{description}\n\ncreated_by_calendar_bot",
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Manila',
        },
        'end': {
            'dateTime': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
            'timeZone': 'Asia/Manila',
        }
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"✅ Event created: {created_event.get('summary')} at {created_event.get('start').get('dateTime')}")

# Example usage
if __name__ == '__main__':
    run_date = datetime(2025, 4, 10, 18, 0)  # change this per event
    create_training_event(
        summary="Zone 2 Run - 5 km",
        description="Part of your half marathon training schedule.",
        start_time=run_date
    )
