from datetime import datetime,timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

async def getCalendarEvents(dateMeasurement):
    result = "```Here are the upcoming events this week: \n"
    result += callCalendarApi(getDayRange(dateMeasurement))
    result += "```"
    return result


def callCalendarApi(dayRange):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=dayRange[0],timeMax=dayRange[1],
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    result = ""

    if not events:
        result += "No upcoming events found."
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        result += start + " " +  event['summary'] + "\n"
    
    return result

def getDayRange(dateMeasurement):
    startDayOffset = 0
    endDayOffset = 0
    dateMeasurement = dateMeasurement.lower()

    if dateMeasurement == "today":
        endDayOffset = 1
    elif dateMeasurement == "tomorrow":
        endDayOffset = 2
        startDayOffset = 1        
    elif dateMeasurement == "week":
        endDayOffset = 7
    else:
        raise ValueError("Date Measurement must be one of the following: today|tomorrow|week")
    
    startDay = (datetime.utcnow() + timedelta(days=startDayOffset)).isoformat("T") + "Z"
    endDay = (datetime.utcnow() + timedelta(days=endDayOffset)).isoformat("T") + "Z"

    return startDay, endDay

def main():
    print(getCalendarEvents(getDayRange("today")))

if __name__ == '__main__':
    main()