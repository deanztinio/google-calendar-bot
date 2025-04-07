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
@app.route('/delete-training-events', methods=['POST'])
def delete_training_events():
    service = get_calendar_service()

    time_min = datetime(2025, 4, 1).isoformat() + 'Z'
    time_max = datetime(2025, 6, 10).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    count = 0
    for event in events:
        summary = event.get("summary", "")
        if any(keyword in summary for keyword in ["Run", "Training", "Race"]):
            service.events().delete(calendarId='primary', eventId=event['id']).execute()
            count += 1

    return jsonify({"deleted_events": count})

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    return build('calendar', 'v3', credentials=creds)

@app.route('/sync-training-plan', methods=['GET'])
def sync_training_plan():
    service = get_calendar_service()

    training_plan = [
        ("2025-04-04", "Zone 2 Run - 5 km"),
        ("2025-04-05", "Strength Training (Crossover)"),
        ("2025-04-06", "CCLEX Scenic Run - 8.3 km"),
        ("2025-04-07", "Rest Day"),
        ("2025-04-08", "Zone 2 Run - 5 km"),
        ("2025-04-09", "Easy 5 km (Beach Run, Bali)"),
        ("2025-04-10", "Easy 5 km (Beach Run, Bali)"),
        ("2025-04-11", "Easy 5 km (Beach Run, Bali)"),
        ("2025-04-12", "Strength Training (Crossover)"),
        ("2025-04-13", "Easy 5 km (Beach Run, Bali)"),
        ("2025-04-14", "Rest Day"),
        ("2025-04-15", "Zone 2 Run - 5 km"),
        ("2025-04-16", "Zone 2 Run - 5 km"),
        ("2025-04-17", "Zone 2 Run - 5 km"),
        ("2025-04-18", "Zone 2 Run - 5 km"),
        ("2025-04-19", "Strength Training (Crossover)"),
        ("2025-04-20", "Long Run - 10 km"),
        ("2025-04-21", "Rest Day"),
        ("2025-04-22", "Zone 2 Run - 5 km"),
        ("2025-04-23", "Zone 2 Run - 5 km"),
        ("2025-04-24", "Zone 2 Run - 5 km"),
        ("2025-04-25", "Zone 2 Run - 5 km"),
        ("2025-04-26", "Strength Training (Crossover)"),
        ("2025-04-27", "Earth Day Run - 10 km Race 🏁"),
        ("2025-04-28", "Rest Day"),
        ("2025-04-29", "Zone 2 Run - 5 km"),
        ("2025-04-30", "Zone 2 Run - 5 km"),
        ("2025-05-01", "Zone 2 Run - 5 km"),
        ("2025-05-02", "Zone 2 Run - 5 km"),
        ("2025-05-03", "Strength Training (Crossover)"),
        ("2025-05-04", "EastWest Dream Run - 13 km Race 🏁"),
        ("2025-05-05", "Rest Day"),
        ("2025-05-06", "Zone 2 Run - 5 km"),
        ("2025-05-07", "Zone 2 Run - 5 km"),
        ("2025-05-08", "Zone 2 Run - 5 km"),
        ("2025-05-09", "Zone 2 Run - 5 km"),
        ("2025-05-10", "Strength Training (Crossover)"),
        ("2025-05-11", "Pace Run - 10 km"),
        ("2025-05-12", "Rest Day"),
        ("2025-05-13", "Zone 2 Run - 5 km"),
        ("2025-05-14", "Zone 2 Run - 5 km"),
        ("2025-05-15", "Zone 2 Run - 5 km"),
        ("2025-05-16", "Long Run - 16 km"),
        ("2025-05-17", "Strength Training (Crossover)"),
        ("2025-05-18", "Recovery Jog - 5 km"),
        ("2025-05-19", "Rest Day"),
        ("2025-05-20", "Zone 2 Run - 5 km"),
        ("2025-05-21", "Zone 2 Run - 5 km"),
        ("2025-05-22", "Zone 2 Run - 5 km"),
        ("2025-05-23", "Zone 2 Run - 5 km"),
        ("2025-05-24", "Strength Training (Crossover)"),
        ("2025-05-25", "Long Run - 16 km"),
        ("2025-05-26", "Rest Day"),
        ("2025-05-27", "Zone 2 Run - 5 km"),
        ("2025-05-28", "Zone 2 Run - 5 km"),
        ("2025-05-29", "Zone 2 Run - 5 km"),
        ("2025-05-30", "Zone 2 Run - 5 km"),
        ("2025-05-31", "Strength Training (Crossover)"),
        ("2025-06-01", "Pace Run - 8 km"),
        ("2025-06-02", "Rest Day"),
        ("2025-06-03", "Zone 2 Run - 4 km"),
        ("2025-06-04", "Zone 2 Run - 4 km"),
        ("2025-06-05", "Zone 2 Run - 3 km"),
        ("2025-06-06", "Zone 2 Run - 3 km"),
        ("2025-06-07", "Rest Day"),
        ("2025-06-08", "🏁 Half Marathon Race Day - 21.1 km")
    ]
@app.route('/list-training-events', methods=['GET'])
def list_training_events():
    service = get_calendar_service()

    time_min = datetime(2025, 4, 4).isoformat() + 'Z'
    time_max = datetime(2025, 6, 10).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    filtered_events = [
        {
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "summary": e["summary"]
        }
        for e in events
        if any(keyword in e["summary"] for keyword in ["Run", "Training", "Race"])
    ]

    return jsonify(filtered_events)

    for date_str, summary in training_plan:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        start_time = date_obj.replace(hour=18, minute=0)
        end_time = start_time + timedelta(hours=1)

        event = {
            'summary': summary,
            'description': 'Half Marathon Training Plan',
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Manila'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Manila'}
        }

        service.events().insert(calendarId='primary', body=event).execute()

    return jsonify({"status": "success", "message": "Training plan events added to calendar."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
