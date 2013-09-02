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


class PlaceProSqlToJsonAdapter(object):

    id_index = 0
    posting_title_index = 1
    company_name_index = 2
    url_index = 3
    location_index = 4
    deadline_index = 5
    job_description_index = 6
    contains_keyword_index = 7

    keyword_color = "ff7537"
    no_keyword_color = "fad165"

    def __init__(self):
        pass

    def convert_sql_tuple_to_json(self, sql_tuple,
        to_json=True):
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
        json_cal = dict()
        
        # We can use the same for both start and end dates because they are going to be all day events
        # and have the same format
        date_dict = { "date" : event_date }

        return { "start" : date_dict, "end" : date_dict }

# a = (389328,
#  u'W14 IBM Co-op General Posting 389328 Online',
#  u'IBM Canada Ltd.',
#  u'www.ibm.com',
#  u'Canada - BC - Vancouver Island',
#  u'Sep 30, 2013',
#  u"Please apply on the IBM website AND PlacePro with all the required documents.\n\nCompany: IBM Canada\nLength: 4, 8, 12, 16 months\nApply online via this website: https://jobs3.netmedia1.com/cp/faces/job_search\n=====================\n\nYou're ambitious. You've got a passion for business.\n\nYou want to work for a company where you're challenged on a daily basis and where you'll get genuine responsibility from day one.\n\nMaybe you want to develop cool technologies and software?\nMaybe you want to leverage your degree or diploma and apply it to the world of business?\nMaybe you want to work for a company that allows you to give something back to the community?\n\nWhatever you want out of your career, you can achieve it at IBM.\n \nWhether you're an undergraduate or post-graduate, we'll help you turn your years of study into tangible achievements through a vast array of global career opportunities and development programs.\n\nStart building the career you want at one of the most successful companies in history.\n\nJoin us. Let's build a Smarter Planet\n \nPlease apply directly on IBM\u2019s website at https://jobs3.netmedia1.com/cp/faces/job_search.\n\nHere are some of the positions currently available on the website:\nSoftware Developer Rational System Architect (4-8 Month Coop) - Kanata\nQA Software Developer Coop, Toronto 4/8 Months May 2013\nQRadar Demo Developer 4-8 Month Coop (Fredericton)\nSoftware Developer - 4-8 Month Coop (Markham)\nIBM Social Media Intern - May 4 month coop (Ottawa)\nIBM Rational Java/Eclipse Software Developer, 4 month Co-op Student 2013 (Markham)\nBusiness Process Management (BPM): Java / Web 2.0 Software Developer \u2013 16 month Internship (Markham)\nTo qualify for student opportunities, applicants must be enrolled at an accredited University or College pursuing a diploma or bachelor/post grad degree. Students must be returning to school after their work term placement to be qualified for a student position. We hire students for4, 8, 12 and 16 month work terms (depending on the type of student placement), which start in January, May, or September.",
#  1,
#  0)

# cal = PlaceProSqlToJsonAdapter()
# print cal.convert_sql_tuple_to_json(a, to_json=True)