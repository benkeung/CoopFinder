from DataRetriever import placepro, indeed, talentegg
from selenium import webdriver

import config
import time

def placepro_runner(
    browser=None,
    keywords=None):

    if not browser:
        browser = webdriver.Chrome()
    placepro_browser = placepro.PlacePro(browser=browser)

    # If we dont specify any keywords, just take in a list with a None
    # so it searches once without any keywords
    if not keywords:
        keywords = [None]

    try:
        placepro_browser.goto_login_page()
        placepro_browser.login()

        for keyword in keywords:
            print "Getting jobs for keyword: %s" % str(keyword)

            placepro_browser.navigate_to_job_search()
            placepro_browser.search_for_computer_science_jobs(keyword=keyword)
            placepro_browser.go_through_all_job_pages()

    finally:
        time.sleep(5)
        placepro_browser.browser.close()


def indeed_runner():
    browser = webdriver.Chrome()
    indeed_browser = indeed.Indeed(browser=browser)

    try:
        indeed_browser.search_for_job("software coop", "toronto")
    finally:
        indeed_browser.browser.close()

def talentegg_runner():
    browser = webdriver.Chrome()
    talentegg_browser = talentegg.TalentEgg(browser=browser)

    try:
        talentegg_browser.goto_job_search_page()
        talentegg_browser.filter_jobs()
    finally:
        talentegg_browser.browser.close()

keywords = config.keywords
# talentegg_runner()
placepro_runner(keywords=keywords)
