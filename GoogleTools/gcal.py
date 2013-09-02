import sys
import os
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(project_root)

import config

import calendar
import gflags
import httplib2
import json
import re

from collections import OrderedDict
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

    def list_events(self, calid=config.default_cal_id):
        events = self.service.events().list(calendarId=calid).execute()
        return events

    def create_event(self, event, calid=config.default_cal_id):
        # event is a dictionary
        response = self.service.events().insert(calendarId=calid, body=event).execute()
        return response

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

class PlaceProSqlToJsonAdapter(object):

    id_index = 0
    posting_title_index = 1
    company_name_index = 2
    url_index = 3
    location_index = 4
    deadline_index = 5
    job_description_index = 6
    contains_keyword_index = 7

    keyword_color = "10"
    no_keyword_color = "5"

    def __init__(self):
        pass

    def convert_sql_tuple_to_json(self, sql_tuple,
        to_json=False):
        """
        :param sql_tuple: is the tuple data returned from querying the 'placepro' table        
        """
        event_date_unformatted = sql_tuple[self.deadline_index]
        event_date = self.__format_date(event_date_unformatted)

        color_id = self.no_keyword_color
        if sql_tuple[self.contains_keyword_index]:
            color_id = self.keyword_color

        event_dictionary = self.__create_basic_dictionary(event_date)

        event_dictionary["summary"] = self.__create_calendar_summary_name(
            sql_tuple[self.company_name_index],
            sql_tuple[self.posting_title_index])
        event_dictionary["description"] = sql_tuple[self.job_description_index]
        event_dictionary["colorId"] = color_id
        event_dictionary["location"] =  sql_tuple[self.location_index]

        if to_json:
            return json.dumps(event_dictionary)

        return event_dictionary

    def __create_calendar_summary_name(self, company_name, posting_title):
        """ Produces 'company_name: post_title' """
        # TODO: Not sure if I need to have these two string replace or not
        company_name = company_name.replace("\\n", r"\n")
        posting_title = posting_title.replace("\\n", r"\n")
        return "%s: %s" % (company_name, posting_title)

    def __format_date(self, date_unformatted):
        """ ie. Conversts 'Sep 30, 2013' to '2013-09-30'"""
        # Creates a dict in format: ie. {"Jan" : 1, "Feb" : 2,...}
        month_converter = {v: k for k,v in enumerate(calendar.month_abbr)}

        date_split = date_unformatted.split()

        month = str(month_converter[date_split[0]])
        date = str(date_split[1][:-1]) # Because the last char is a comma
        year = str(date_split[2])

        return "%s-%s-%s" % (year, month, date)

    def __create_basic_dictionary(self, event_date, 
        to_json=False):
        """
        :param event_date: date format in yyyy-mm-dd
        """
        event_date = str(event_date)
        
        # We can use the same for both start and end dates because they are going to be all day events
        # and have the same format
        date_dict = { "date" : event_date }
        js_dict = {"start": date_dict, "end": date_dict}

        return js_dict
