# app.py

from flask import Flask, request
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'token.pkl'

CREDENTIALS = {
    "installed": {
        "client_id": "1023408752441-osic1fbv1vb185sjo1jfjt74m12kasjq.apps.googleusercontent.com",
        "client_secret": "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",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    return build('calendar', 'v3', credentials=creds)

def create_zone2_event():
    service = get_calendar_service()
    tomorrow = datetime.now() + timedelta(days=1)
    start_time = tomorrow.replace(hour=6, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': 'Zone 2 Run',
        'description': 'Automated event from Render',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Manila'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Manila'}
    }

    service.events().insert(calendarId='primary', body=event).execute()

# Flask app
app = Flask(__name__)

@app.route('/update-calendar', methods=['POST'])
def update_calendar():
    create_zone2_event()
    return {'status': '✅ Calendar updated successfully!'}

if __name__ == '__main__':
    app.run()
