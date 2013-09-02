from DataHandlers import data_handler
from DataRetriever import placepro
from GoogleTools import gcal

from selenium import webdriver

import config

def placepro_runner():
    # Appending an empty string because we want to also get all the jobs after
    keywords = [""] + config.keywords

    browser = webdriver.Chrome()

    try:
        placepro_browser = placepro.PlacePro(browser=browser, login_credentials=config.placepro_login)
        datahandler = data_handler.DataHandler()

        placepro_browser.goto_login_page()
        placepro_browser.login()

        for keyword in keywords:
            print "Getting jobs for keyword: %s" % str(keyword)

            placepro_browser.navigate_to_job_search()
            placepro_browser.search_for_computer_science_jobs(keyword=keyword)

            # We want keyworded events to always take precedence. So whenever we see that an
            # event has a keyword, we should override it in case it's not already keyword-tagged
            if keyword:
                placepro_browser.go_through_all_job_pages(
                    function_for_page=datahandler.insert_placepro_adapter_overwrite_keyword_flag)
            else:
                placepro_browser.go_through_all_job_pages(
                    function_for_page=datahandler.insert_placepro_adapter)

    finally:
        datahandler.connection.close()
        placepro_browser.browser.close()

def placepro_data_runner():
    # named gcal2 because gcal is a module that's already being imported in
    gcal2 = gcal.GoogleCalender()
    adapter = gcal.PlaceProSqlToJsonAdapter()

    try:
        sql_handler = data_handler.DataHandler()
        all_placepro_tuples = sql_handler.get_all_placepro()

        for placepro_tuple in all_placepro_tuples:
            placepro_id  = placepro_tuple[0]

            if not sql_handler.is_in_calendar(placepro_id):
                placepro_js = adapter.convert_sql_tuple_to_json(placepro_tuple, False)

                gcal2.create_event(placepro_js, config.placepro_coop_cal_id)
                sql_handler.set_in_calendar(placepro_id, in_calendar=1)
    finally:
        sql_handler.close_connection()

placepro_runner()
placepro_data_runner()
