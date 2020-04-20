import time
from random import uniform, shuffle, seed
import re
import collections
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


seed(version=2)
CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument("--incognito")
CHROME_OPTIONS.add_argument("--lang=en")
DRIVER_1 = {"Chrome": webdriver.Chrome(
    chrome_options=CHROME_OPTIONS,
    executable_path=ChromeDriverManager().install())}
DRIVER_2 = {"Chrome": webdriver.Chrome(
    chrome_options=CHROME_OPTIONS,
    executable_path=ChromeDriverManager().install())}
LINKEDIN_URL = "https://www.linkedin.com"
TIME_SLEEP_GAP_1 = [5, 8]
TIME_SLEEP_GAP_2 = [1, 2]
TIMES_PARAMETERS = {
    "Past 24 hours": "r86400",
    "Past Week": "r604800",
    "Past Month": "r2592000"}


class BotJobsId():

    def __init__(self, driver, user, password):

        self.driver = DRIVER_1[driver]
        self.user = user
        self.password = password

    def get_jobs_id(self, job_search_specifics):

        self.log_in()
        BotJobsId.sleep()
        jobs_id = self.get_ids(job_search_specifics)
        shuffle(jobs_id)

        return jobs_id

    def log_in(self) -> None:

        self.driver.get(LINKEDIN_URL + "/login")
        user = self.driver.find_element_by_id("username")
        user.send_keys(self.user)
        password = self.driver.find_element_by_id("password")
        password.send_keys(self.password)
        password.submit()

    @staticmethod
    def sleep():

        time.sleep(uniform(TIME_SLEEP_GAP_1[0], TIME_SLEEP_GAP_1[1]))

    def get_ids(self, job_search_specifics):

        jobs_url = BotJobsId.get_jobs_url(job_search_specifics)
        self.driver.get(jobs_url)
        BotJobsId.sleep()

        pages = self.driver.find_elements_by_xpath(
            '//section[@class="jobs-search-two-pane__pagination"]//button[@aria-label]')
        last_page = int(pages[-1].get_attribute("aria-label").split(" ")[1])

        jobs_id = []
        page_number = 1

        while page_number < 41:
            try:
                print(page_number)
                page = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, f"//button[@aria-label='Page {page_number}']")))
                page.click()
                BotJobsId.sleep()
                self.scroll_job_list()
                BotJobsId.sleep()
                html_code = self.driver.page_source
                soup = BeautifulSoup(html_code, "lxml")
                jobs_id_page_html = soup.select("div[data-job-id]")
                jobs_id_page = [
                    job_id["data-job-id"].split(":")[-1] for job_id in jobs_id_page_html]
                jobs_id = jobs_id + jobs_id_page
                BotJobsId.sleep()
                self.check_repeated_elements(jobs_id)
                page_number += 1
            except:
                if page_number == (last_page + 1):
                    break
                page_number -= 1
                print(page_number)
                jobs_url_page = jobs_url + "&start=" + str(25*page_number)
                self.driver.get(jobs_url_page)

        jobs_id_not_repeated = list(dict.fromkeys(jobs_id))

        return jobs_id_not_repeated

    @staticmethod
    def get_jobs_url(job_search_specifics):

        if job_search_specifics["time_range"] != "Any Time":
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" + "f_E=2%2C3%2C4&" +
                "f_TPR=" + TIMES_PARAMETERS[job_search_specifics["time_range"]] +
                "&keywords=" +
                BotJobsId.adapt_words(job_search_specifics["key_words"]) + "%2C%20"
                "&location=" +
                BotJobsId.adapt_words(job_search_specifics["location"])
            )
        else:
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" + "f_E=2%2C3%2C4&" +
                "&keywords=" +
                BotJobsId.adapt_words(job_search_specifics["key_words"]) + "%2C%20"
                "&location=" +
                BotJobsId.adapt_words(job_search_specifics["location"])
            )

        return job_list_url

    @staticmethod
    def adapt_words(parameter):

        adapted_parameter = parameter.replace(" ", "%20")

        return adapted_parameter

    def scroll_job_list(self):

        jobs_list = self.driver.find_element_by_class_name("jobs-search-results")
        half_stopped = int(uniform(0, 300))
        for piece in range(0, half_stopped):
            self.driver.execute_script(f"arguments[0].scrollTo(0, {10 * piece})", jobs_list)
        BotJobsId.sleep()
        for piece in range(half_stopped, 300):
            self.driver.execute_script(f"arguments[0].scrollTo(0, {10 * piece})", jobs_list)

    def close_driver(self):

        self.driver.close()

    @staticmethod
    def check_repeated_elements(jobs_to_check):

        repeated_elements = [
            job for job, count in collections.Counter(jobs_to_check).items() if count > 1]
        print("repeated_elements", repeated_elements)

class BotJobsData():

    def __init__(self, driver):

        self.driver = DRIVER_2[driver]

    def get_jobs_data(self, jobs_id):

        jobs_data = []

        for job_id in jobs_id:

            job_data = {}

            try:
                job_data["id"] = job_id
                self.driver.get(BotJobsData.get_one_job_url(job_id))
                BotJobsData.sleep()
                src = self.driver.page_source.encode("utf-8")
                soup = BeautifulSoup(src, "lxml")
                BotJobsData.get_top_card_data(soup, job_data)
                try:
                    text = soup.find("div", {"class":"description__text"}).getText()
                    job_data["text"] = text
                except:
                    print(job_id, " has no text")
                BotJobsData.get_jobs_details_data(soup, job_data)
            except:
                print("warning connection")

            jobs_data.append(job_data)

        return jobs_data

    @staticmethod
    def get_one_job_url(job_id):

        job_url = LINKEDIN_URL + "/jobs/view/" + job_id

        return job_url

    @staticmethod
    def get_top_card_data(soup, job_data):

        try:
            title = soup.find("h1", {"class":"topcard__title"}).getText()
            job_data["title"] = title
        except:
            print(job_data["id"], " has no title")
        try:
            company = soup.find("span", {"class":"topcard__flavor"}).getText()
            job_data["company"] = company
        except:
            print(job_data["id"], " has no company")
        try:
            location = soup.find("span", {"class":"topcard__flavor--bullet"}).getText()
            job_data["location"] = location
        except:
            print(job_data["id"], " has no location")
        try:
            posted = soup.find("span", {"class":"posted-time-ago__text"}).getText()
            posted = re.search(
                '(.*)ago', posted).group(1)
            job_data["posted"] = BotJobsData.get_days(posted)
        except:
            print(job_data["id"], " has no posted")
        try:
            applicants = soup.find("span", {"class":"num-applicants__caption"}).getText()
            applicants = re.search(
                '(.*)applicants', applicants).group(1)
            job_data["applicants"] = applicants
        except:
            job_data["applicants"] = "0"


    @staticmethod
    def get_jobs_details_data(soup, job_data):

        job_details = soup.find("ul", {"class":"job-criteria__list"}).getText()
        job_details = re.sub(r"([a-z])([A-Z])", r"\1 \2", job_details)
        try:
            job_data["level"] = re.search(
                'level(.*)Employment type', job_details).group(1)
        except:
            print(job_data["id"], " has no level")
        try:
            job_data["type"] = re.search(
                'Employment type(.*)Job function', job_details).group(1)
        except:
            print(job_data["id"], " has no type")
        try:
            job_data["functions"] = re.search(
                'Job function(.*)Industries', job_details).group(1)
        except:
            print(job_data["id"], " has no functions")
        try:
            job_data["industries"] = re.search(
                'Industries(.*)', job_details).group(1)
        except:
            print(job_data["id"], " has no industries")

    @staticmethod
    def get_days(name):

        switcher = {
            "hours": float(name.split(" ")[0])/24,
            "hour": float(name.split(" ")[0])/24,
            "days": float(name.split(" ")[0]),
            "day": float(name.split(" ")[0]),
            "week": float(name.split(" ")[0])*7,
            "weeks": float(name.split(" ")[0])*7,
            "months": float(name.split(" ")[0])*30,
            "month": float(name.split(" ")[0])*30
            }

        return switcher.get(name.split(" ")[1], "Invalid day of week")

    def close_driver(self):

        self.driver.close()

    @staticmethod
    def sleep():

        time.sleep(uniform(TIME_SLEEP_GAP_2[0], TIME_SLEEP_GAP_2[1]))
