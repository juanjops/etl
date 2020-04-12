import time
import re
from random import uniform
import collections
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


class Linkedinbot():

    def __init__(self, driver):

        self.driver = DRIVERS[driver]

    def get_jobs_data(self, job_search_specifics):

        jobs_url = Linkedinbot.get_jobs_url(job_search_specifics)
        self.driver.get(jobs_url)
        Linkedinbot.sleep()
        self.scroll()
        jobs_id = self.get_jobs_id()
        Linkedinbot.sleep()
        jobs_data = self.get_jobid_texts(jobs_id, job_search_specifics)
        Linkedinbot.sleep()

        return jobs_data

    @staticmethod
    def sleep() -> None:

        time.sleep(uniform(TIME_SLEEP_GAP[0], TIME_SLEEP_GAP[1]))

    def get_jobs_id(self):


        html_code = self.driver.page_source
        soup = BeautifulSoup(html_code, "lxml")
        jobs_id_html = soup.select("li[data-id]")
        jobs_id = [job_id["data-id"] for job_id in jobs_id_html]
        self.check_repeated_elements(jobs_id)
        jobs_id_not_repeated = list(dict.fromkeys(jobs_id))

        return jobs_id_not_repeated

    @staticmethod
    def get_jobs_url(job_search_specifics):

        job_list_url = (
            LINKEDIN_URL + "/jobs/search/?" +
            "keywords=" + Linkedinbot.adapt_words(job_search_specifics["position"]) + "%2C%20"
            "&location=" + Linkedinbot.adapt_words(job_search_specifics["city"]) + "%2C%20" +
            Linkedinbot.adapt_words(job_search_specifics["region"]) + "%2C%20" +
            Linkedinbot.adapt_words(job_search_specifics["country"]) +
            "&trk=public_jobs_jobs-search-bar_search-submit&" +
            TIMES_PARAMETERS[job_search_specifics["time_range"]] +
            "&redirect=false&position=1&pageNum=0"
        )

        return job_list_url

    @staticmethod
    def adapt_words(parameter):

        adapted_parameter = parameter.replace(" ", "%20")

        return adapted_parameter

    def scroll(self) -> None:

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Linkedinbot.sleep()
            try:
                self.driver.find_element_by_xpath(
                    "//button[@aria-label='Load more results']").click()
            except:
                pass
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    @staticmethod
    def check_repeated_elements(jobs_to_check) -> None:

        repeated_elements = [
            job for job, count in collections.Counter(jobs_to_check).items() if count > 1]
        if len(repeated_elements) != 0:
            print("repeated_elements", repeated_elements)

    def get_jobid_texts(self, jobs_id, job_search_specifics):

        jobs_data = []

        jobs_card = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located((
                By.XPATH,
                ("//ul[@class='jobs-search__results-list']" +
                 "//a[@class='result-card__full-card-link']"))))

        if len(jobs_card) != len(jobs_id):

            print(job_search_specifics, "ids and cards not the same")

        for job_id, job_card in zip(jobs_id, jobs_card):

            job_card.click()
            Linkedinbot.sleep()
            job_data = {}
            job_data["id"] = job_id
            src = self.driver.page_source.encode("utf-8")
            soup = BeautifulSoup(src, "lxml")
            try:
                text = soup.find("div", {"class":"description__text"}).getText()
                job_data["text"] = text
            except:
                print(job_id, " has no text")
            Linkedinbot.get_top_card_data(soup, job_data)
            Linkedinbot.get_jobs_details_data(soup, job_data)
            jobs_data.append(job_data)

        return jobs_data

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

    @staticmethod
    def get_one_job_url(job_id):

        job_url = LINKEDIN_URL + "/jobs/view/" + job_id

        return job_url

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

    def close_driver(self) -> None:

        self.driver.close()
