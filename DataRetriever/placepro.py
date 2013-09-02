import re
import login

from getpass import getpass
from time import sleep
from base_site import BaseJobSite
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

class PlacePro(BaseJobSite):

    url = "http://www.placeprocanada.com"

    def __init__(self, 
        login_credentials=None,
        browser=None):

        # NOTE: We have to use Chrome because Firefox's back does not allow for 
        # sensitive information apparently
        if not browser:
            browser = webdriver.Chrome()
        
        if not login_credentials:
            login_credentials = dict()
            login_credentials["access_code"] = "UBCSTUDENT"
            login_credentials["username"] = raw_input("PlacePro Username: ")
            login_credentials["password"] = getpass("PlacePro Password (input is hidden): ")

        super(PlacePro, self).__init__(browser)

        self.login_credentials = login_credentials
        self.browser.get(self.url)

    def goto_login_page(self):
        """ Go to the PlacePro site """
        student_login_button = self.browser.find_element_by_css_selector(
            "a[title='Login to the Student Module']")
        student_login_button.click()

    def login(self):
        """ Log into the PlacePro site"""
        login_input = self.browser.find_element_by_css_selector(
            "input[name='txtLogin']")
        password_input = self.browser.find_element_by_css_selector(
            "input[name='txtPassword']")
        access_code_input = self.browser.find_element_by_css_selector(
            "input[name='txtAccessCode']")
        login_button = self.browser.find_element_by_id(
            "btnLogin")

        login_input.clear()
        login_input.send_keys(self.login_credentials["username"])

        password_input.clear()
        password_input.send_keys(self.login_credentials["password"])

        access_code_input.clear()
        access_code_input.send_keys(self.login_credentials["access_code"])

        login_button.click()

    def navigate_to_job_search(self):
        job_search_button = self.browser.find_element_by_id(
            "ctl00_hypTopJobs")
        job_search_button.click()

    def search_for_computer_science_jobs(self,
                                         keyword=None):
        # Term is a school term
        term_of_interest = self.browser.find_element_by_css_selector(
            "select[id='ctl00_conHF_ppcboEmpType_cbo'] option[value='1;2;2014;0']")
        term_of_interest.click()

        # Choose to include only computer science jobs
        cpsc_jobs_checkbox = self.browser.find_element_by_id(
            r"ctl00_conHF_pplstMajors_lst_15")
        cpsc_jobs_checkbox.click()

        # Select the "You have not made a selection" button2
        selection_button = self.browser.find_element_by_css_selector(
            r"select[id='ctl00_conHF_ppcboApply_cbo'] option[value='-3']")
        selection_button.click()

        # Select for order by deadline
        deadline_option = self.browser.find_element_by_css_selector(
            r"select[id='ctl00_conHF_ppcboSortBy_cbo'] option[value='3']")
        deadline_option.click()

        if keyword:
            keyword_input = self.browser.find_element_by_id(
                "ctl00_conHF_pptxtKeyword_txt")
            keyword_input.clear()
            keyword_input.send_keys(keyword)

            # Set a class variable flag that indicates whether we are searching for a keyword
            self.keyword_flag = True
        else:
            self.keyword_flag = False

        search_button = self.browser.find_element_by_css_selector(
            r"input[name='ctl00$conHF$cmdQuickSearch']")

        search_button.click()

        # Do some work to handle the popup
        try:
            alert = self.browser.switch_to_alert()
            alert.accept()
        except NoAlertPresentException:
            pass

    def go_through_all_job_pages(self, function_for_page=None):
        """ Navigates through all the possible job sea
        """
        if not function_for_page:
            function_for_page = super(PlacePro, self).pretty_dictionary_print

        self.__goto_individual_job_pages(function_for_page)
        page_flipper = self.__page_flipper_generator()

        for page in page_flipper:
            print "At page %s" % str(page)
            self.__goto_individual_job_pages(function_for_page)


    def page_parse_to_dictionary(self,
        placepro_id=None):
        """ Parse a specific job posting into a dictionary
        """

        # If not passed a place pro id, we should try to get one from here
        if not placepro_id:
            placepro_id_regex = re.search(r"(\d{6})", posting_title)
            if placepro_id_regex:
                placepro_id = place_pro_id_regex.group(1)

        posting_title = self.browser.find_element_by_id(
            "ctl00_conHF_lblJobTitle").text
        
        company_name = self.browser.find_element_by_id(
            "ctl00_conHF_lblCompanyName").text
        url = self.browser.find_element_by_id(
            "ctl00_conHF_lnkWWWURL").text
        location = self.browser.find_element_by_id(
            "ctl00_conHF_lblLocation").text
        resume_deadline = self.browser.find_element_by_id(
            "ctl00_conHF_lblDeadline").text
        job_description = self.browser.find_element_by_css_selector(
            "div[class='ToolBoxInner'] div[class='JobDescrip']").text

        job_information = { "id": placepro_id,
                            "posting_title": posting_title,
                            "company_name": company_name,
                            "url": url,
                            "location": location,
                            "resume_deadline": resume_deadline,
                            "job_description": job_description,
                            "contains_keyword": self.keyword_flag,
                            }
        return job_information

    def __page_flipper_generator(self):
        """
        Creates a generator object that flips through all the pages.
        """
        page_number = 1
        while True:
            try:
                page_number += 1

                next_page_link = self.browser.find_element_by_link_text(
                    str(page_number))
                next_page_link.click()
                yield page_number

            except NoSuchElementException:
                print "End of flipping through the navigation of pages."
                break

    def __goto_individual_job_pages(self, function_for_page):
        job_links = self.browser.find_elements_by_css_selector(
            "a.BlueLinkLG")
        job_names = [job_link_element.text for job_link_element in job_links]

        for job_name in job_names:
            job_link = self.browser.find_element_by_link_text(job_name)
            
            placepro_id = None
            placepro_posting_id_regex = re.search(r"(\d{6})", job_name)
            if placepro_posting_id_regex:
                placepro_id = placepro_posting_id_regex.group(1)

            job_link.click()
            posting = self.page_parse_to_dictionary(placepro_id=placepro_id)
            function_for_page(posting)
            self.browser.back()
