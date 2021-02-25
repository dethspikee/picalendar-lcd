from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events(number: int) -> list:
    """
    Retrieve 'number' of events from Google Calendar API
    and return list of events
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    token_path = os.path.join(dir_path, 'token.pickle')
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {number} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=number, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    upcoming = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        upcoming.append({
                "start": start,
                "summary": event["summary"]
            })

    if len(upcoming) == 0:
        print('No upcoming events...')

    return upcoming 
