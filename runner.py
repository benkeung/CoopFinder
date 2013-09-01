from DataHandlers import data_handler
from DataRetriever import placepro
from selenium import webdriver

import config

def placepro_runner():
    # Appending an empty string because we want to also get all the jobs after
    keywords = config.keywords + [""]

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
            placepro_browser.go_through_all_job_pages(function_for_page=datahandler.insert_placepro_adapter)

    finally:
        datahandler.connection.close()
        placepro_browser.browser.close()

placepro_runner()