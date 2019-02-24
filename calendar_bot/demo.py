"""Demo app."""

from __future__ import print_function

from googleapiclient.discovery import build

from calendar_bot.calendar import get_creds, get_events_last_24h


def main():
    """
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    events = get_events_last_24h(service)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
