# import sys
# import os
# project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# sys.path.append(project_root)

# import config

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import httplib2

# class GoogleCalender(object):

#     def __init__(self):
#         self.flow = OAuth2WebServerFlow(
#             client_id=config.client_id,
#             client_secret=config.client_secret,
#             scope='https://www.googleapis.com/auth/calendar',
#             user_agent=config.user_agent)

#         self.__build_service()

#     def __build_service(self):
#         http = httplib2.Http()
#         http = credentials.authorize(http)

#         self.service = build(
#             sevice_name="calendar",
#             version="v3",
#             http=http,
#             developerKey=config.developer_key)
