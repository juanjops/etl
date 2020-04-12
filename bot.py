import time
from random import uniform, shuffle
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument("--incognito")
CHROME_OPTIONS.add_argument("--lang=en")
DRIVERS = {"Chrome": webdriver.Chrome(
    chrome_options=CHROME_OPTIONS,
    executable_path=ChromeDriverManager().install())}
LINKEDIN_URL = "https://www.linkedin.com"
TIME_SLEEP_GAP = [0.5, 1.5]
TIMES_PARAMETERS = {
    "Past 24 hours": "f_TP=1",
    "Past Week": "f_TP=1%2C2",
    "Past Month": "f_TP=1%2C2%2C3%2C4",
    "Any Time": ""}


class bot_jobs_id():

    def __init__(self, driver, user, password):

        self.driver = DRIVERS[driver]
        self.user = user
        self.password = password

    def get_jobs_id(self, job_search_specifics):

        self.log_in()
        bot_jobs_id.sleep()
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
    def sleep() -> None:

        time.sleep(uniform(TIME_SLEEP_GAP[0], TIME_SLEEP_GAP[1]))

    def get_ids(self, job_search_specifics):

        jobs_url = bot_jobs_id.get_jobs_url(job_search_specifics)
        self.driver.get(jobs_url)
        jobs_id = []
        page_number = 1

        while page_number < 100:
            try:
                page = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, f'//button[@aria-label="Page {page_number}"]')))
                page.click()
                bot_jobs_id.sleep()
                self.scroll_job_list()
                html_code = self.driver.page_source
                soup = BeautifulSoup(html_code, "lxml")
                jobs_id_page_html = soup.select("div[data-job-id]")
                jobs_id_page = [
                    job_id["data-job-id"].split(":")[-1] for job_id in jobs_id_page_html]
                jobs_id = jobs_id + jobs_id_page
                self.check_repeated_elements(jobs_id)
            except:
                break
            page_number += 1
            bot_jobs_id.sleep()

        jobs_id_not_repeated = list(dict.fromkeys(jobs_id))

        return jobs_id_not_repeated

    @staticmethod
    def get_jobs_url(job_search_specifics):

        if job_search_specifics["time_range"] != "Any Time":
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" +
                "f_TPR=" + TIMES_PARAMETERS[job_search_specifics["time_range"]] +
                "&keywords=" + bot_jobs_id.adapt_words(job_search_specifics["position"]) + "%2C%20"
                "&location=" + bot_jobs_id.adapt_words(job_search_specifics["city"]) + "%2C%20" +
                bot_jobs_id.adapt_words(job_search_specifics["region"]) + "%2C%20" +
                bot_jobs_id.adapt_words(job_search_specifics["country"])
            )
        else:
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" +
                "&keywords=" + bot_jobs_id.adapt_words(job_search_specifics["position"]) + "%2C%20"
                "&location=" + bot_jobs_id.adapt_words(job_search_specifics["city"]) + "%2C%20" +
                bot_jobs_id.adapt_words(job_search_specifics["region"]) + "%2C%20" +
                bot_jobs_id.adapt_words(job_search_specifics["country"])
            )

        return job_list_url

    @staticmethod
    def adapt_words(parameter):

        adapted_parameter = parameter.replace(" ", "%20")

        return adapted_parameter

    def scroll_job_list(self) -> None:

        jobs_list = self.driver.find_element_by_class_name("jobs-search-results")

        for piece in range(0, 10):
            self.driver.execute_script(f"arguments[0].scrollTo(0, {300 * piece})", jobs_list)
            bot_jobs_id.sleep()

    def close_driver(self) -> None:

        self.driver.close()


class bot_jobs_data(bot_jobs_id):

    def __init__(self, driver):

        self.driver = DRIVERS[driver]

    def get_jobs_data(self, jobs_id):

        jobs_data = []

        for job_id in jobs_id:

            job_data = {}

            try:
                job_data["id"] = job_id
                self.driver.get(bot_jobs_data.get_one_job_url(job_id))
                bot_jobs_data.sleep()
                src = self.driver.page_source.encode("utf-8")
                soup = BeautifulSoup(src, "lxml")
                bot_jobs_data.get_top_card_data(soup, job_data)
                try:
                    text = soup.find("div", {"class":"description__text"}).getText()
                    job_data["text"] = text
                except:
                    print(job_id, " has no text")
                bot_jobs_data.get_jobs_details_data(soup, job_data)
            except:
                print("warning connection")

            jobs_data.append(job_data)

        return jobs_data

    @staticmethod
    def get_one_job_url(job_id):

        job_url = LINKEDIN_URL + "/jobs/view/" + job_id

        return job_url

    @staticmethod
    def get_top_card_data(soup, job_data) ->None:

        try:
            title = soup.find("h2", {"class":"topcard__title"}).getText()
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
            job_data["posted"] = Linkedinbot.get_days(posted)
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
    def get_jobs_details_data(soup, job_data) ->None:

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
