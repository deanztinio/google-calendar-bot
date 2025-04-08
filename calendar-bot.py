from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import pickle
from collections import defaultdict

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pkl'

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    return build('calendar', 'v3', credentials=creds)

def remove_duplicate_events():
    service = get_calendar_service()

    calendar_id = 'primary'
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=1000,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    print(f"🧹 Total events fetched: {len(events)}")

    # Group events by (start, summary)
    grouped = defaultdict(list)
    for event in events:
        start = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
        key = (start, event.get('summary'))
        grouped[key].append(event)

    duplicates_removed = 0
    for key, grouped_events in grouped.items():
        if len(grouped_events) > 1:
            # Keep one, delete the rest
            for event in grouped_events[1:]:
                service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
                print(f"🗑️ Deleted duplicate: {event['summary']} at {key[0]}")
                duplicates_removed += 1

    print(f"✅ Cleanup complete. Removed {duplicates_removed} duplicate events.")

if __name__ == '__main__':
    remove_duplicate_events()
