"""Demo calendar interaction."""

from googleapiclient.discovery import build

from calendar_bot.calendar import get_creds, get_events_last_24h, \
    events_filter_keys


def main():
    """
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    events = get_events_last_24h(service)
    events_processed = events_filter_keys(events)

    if not events_processed:
        print('No upcoming events found.')
    else:
        print(f'Found {len(events_processed)} events within last 24 hours:')
        for event in events_processed:
            print('* ' + event['summary'])


if __name__ == '__main__':
    main()
