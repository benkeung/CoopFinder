import sys
import os
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(project_root)

import config
import httplib2
import gflags

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class GoogleCalender(object):
    """
    Official Google documentation: https://developers.google.com/google-apps/calendar/instantiate
    """
    credentials_filename = "calendar.dat"

    def __init__(self):
        self.service = self.__build_service()

    def list_events(self):
        events = self.service.events().list(calendarId="benkeungg@gmail.com").execute()

    def create_event(self, calid, event):
        rec_event = self.service.events().insert(calendarId=calid, body=event).execute()

    def __build_service(self):
        """ Creates the service object and based on the credentials stored in
        config.py """

        flow = OAuth2WebServerFlow(
            client_id=config.client_id,
            client_secret=config.client_secret,
            scope='https://www.googleapis.com/auth/calendar',
            user_agent=config.user_agent)    

        storage = Storage(self.credentials_filename)
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(flow, storage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build(
            serviceName="calendar",
            version="v3",
            http=http,
            developerKey=config.developer_key)

        return service

class CalendarDataAdapter(object):

    def __init__(self):
        pass