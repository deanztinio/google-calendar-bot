from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import pickle

# Token and scope setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pkl'

# Get Google Calendar service
def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    service = build('calendar', 'v3', credentials=creds)
    return service

# Delete events with known training plan titles
def delete_training_events():
    service = get_calendar_service()
    calendar_id = 'primary'

    # Define matching keywords in training titles
    training_keywords = [
        "Zone 2 Run", "Long Run", "Pace Run", 
        "Strength Training", "EastWest Dream Run",
        "Earth Day Run", "CCLEX", "🏁 Half Marathon"
    ]

    events_result = service.events().list(calendarId=calendar_id,
                                          maxResults=500,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    count = 0
    for event in events:
        title = event.get('summary', '')
        if any(keyword in title for keyword in training_keywords):
            try:
                service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
                print(f"🗑️ Deleted: {title}")
                count += 1
            except Exception as e:
                print(f"Failed to delete {title}: {e}")

    print(f"✅ Done! Deleted {count} training events.")

if __name__ == '__main__':
    delete_training_events()
