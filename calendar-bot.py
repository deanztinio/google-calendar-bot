from flask import Flask, jsonify
from datetime import datetime, timedelta
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = Flask(__name__)

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

@app.route('/list-events', methods=['GET'])
def list_events():
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=end,
        maxResults=20, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append({'summary': event.get('summary'), 'start': start})

    return jsonify(event_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
