from selenium.common.exceptions import NoSuchElementException

class Indeed:

    url = "http://www.indeed.ca/"

    def __init__(self, browser,
                 login_credentials=None):
        self.browser = browser
        self.browser.get(self.url)
        self.login_credentials = login_credentials

    def search_for_job(self, search_term, location):
        search_element = self.browser.find_element_by_id("what")
        location_element = self.browser.find_element_by_id("where")
        click_search_button = self.browser.find_element_by_id("fj")

        search_element.clear()
        search_element.send_keys(search_term)

        location_element.clear()
        location_element.send_keys(location)

        click_search_button.click()
