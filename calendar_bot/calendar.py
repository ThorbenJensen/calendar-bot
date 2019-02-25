"""Utils for calendar operations."""

import copy
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
# from calendar_bot.calendar import get_creds
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('secret/token.pickle'):
        with open('secret/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secret/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('secret/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def datetime_to_rfc3339(dt: datetime.datetime) -> str:
    return dt.isoformat() + 'Z'


def get_events_last_24h(service):
    """
    Get calendar events from previous 24 hours, until now.
    :param service:
    :return events:
    """
    time_max = datetime.datetime.utcnow()
    time_min = time_max - datetime.timedelta(days=1.0)

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary',
                                          timeMin=datetime_to_rfc3339(time_min),
                                          timeMax=datetime_to_rfc3339(time_max),
                                          maxResults=100,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def events_filter_keys(events):
    keys_selection = ['id', 'summary', 'start', 'end', 'location',
                      'description']
    events_selected = [{key: event.get(key) for key in keys_selection}
                       for event in events]

    # format fields start and end
    for event in events_selected:
        # start
        event['start_date'] = event['start'].get('date')
        event['start_datetime'] = event['start'].get('dateTime')
        # end
        event['end_date'] = event['end'].get('date')
        event['end_datetime'] = event['end'].get('dateTime')

    events_parsed = copy.deepcopy(events_selected)
    for event in events_parsed:
        if 'start' in event.keys(): del event['start']
        if 'end' in event.keys(): del event['end']

    return events_parsed
