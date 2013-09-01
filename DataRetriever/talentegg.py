from base_site import BaseJobSite
from time import sleep

class TalentEgg(BaseJobSite):

    url = "http://www.talentegg.ca"

    def __init__(self, browser):
        super(TalentEgg, self).__init__(browser)

        self.browser.get(self.url)

    def goto_job_search_page(self):
        find_job_button = self.browser.find_element_by_css_selector(
            "ul[class='nav is-left'] li a[href='/find-a-job/'")
        find_job_button.click()

    def filter_jobs(self,
                    industry=None, province=None, city=None):
        coop_button = self.browser.find_element_by_id("co-op")
        coop_button.click()

        industry_select_box = self.browser.find_element_by_css_selector(
            "div[class='filter'] select[class='selectType industrySelect']")
        industry_select_button = industry_select_box.find_element_by_css_selector("css=option:contains('Technology')")
        industry_select_button.click()

        # industry_technology = self.browser.find_element_by_id("area_Technology")
        # industry_technology.click()
        #
        # province_ontario = self.browser.find_element_by_id("5")
        # province_ontario.click()
        #
        # city_toronto = self.browser.find_element_by_css_selector("option[value='toronto']")
        # city_toronto.click()

        search_button = self.browser.find_element_by_id("searchBtn")
        search_button.click()