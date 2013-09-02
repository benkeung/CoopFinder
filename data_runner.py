from DataRetriever import placepro, indeed, talentegg
from selenium import webdriver

import config
import time

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

