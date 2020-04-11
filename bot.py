import time
import re
from random import shuffle, uniform
import collections
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


DRIVERS = {"Chrome": webdriver.Chrome(executable_path=ChromeDriverManager().install())}
LINKEDIN_URL = "https://www.linkedin.com"
TIME_SLEEP_GAP = [3, 6]
TIMES_PARAMETERS = {
    "Past 24 hours": "r86400",
    "Past Week": "r604800",
    "Past Month": "r2592000"}


class Linkedinbot():

    def __init__(self, driver, user, password):

        self.driver = DRIVERS[driver]
        self.user = user
        self.password = password

    def get_jobs_data(self, job_search_specifics, file_name):

        self.log_in()
        Linkedinbot.sleep()
        jobs_id = self.get_jobs_id(job_search_specifics)
        shuffle(jobs_id)
        Linkedinbot.create_jobs_id_file(jobs_id, file_name)
        Linkedinbot.sleep()
        jobs_data = self.get_jobid_texts(jobs_id)
        Linkedinbot.create_jobs_data_file(jobs_data, file_name)
        Linkedinbot.sleep()
        self.driver.close()

        return jobs_data

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

    def get_jobs_id(self, job_search_specifics):

        jobs_url = Linkedinbot.get_jobs_url(job_search_specifics)
        self.driver.get(jobs_url)
        jobs_id = []
        page_number = 1

        while page_number < 100:
            try:
                page = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, f'//button[@aria-label="Page {page_number}"]')))
                page.click()
                Linkedinbot.sleep()
                self.scroll_job_list()
                html_code = self.driver.page_source
                soup = BeautifulSoup(html_code, "lxml")
                jobs_id_page_html = soup.select("div[data-job-id]")
                jobs_id_page = [
                    job_id["data-job-id"].split(":")[-1] for job_id in jobs_id_page_html]
                jobs_id = jobs_id + jobs_id_page
                self.check_repeated_elements(jobs_id)
            except WebDriverException:
                break
            page_number += 1
            Linkedinbot.sleep()

        jobs_id_not_repeated = list(dict.fromkeys(jobs_id))

        return jobs_id_not_repeated

    @staticmethod
    def get_jobs_url(job_search_specifics):

        if job_search_specifics["time_range"] != "Any Time":
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" +
                "f_TPR=" + TIMES_PARAMETERS[job_search_specifics["time_range"]] +
                "&keywords=" + Linkedinbot.adapt_words(job_search_specifics["position"]) + "%2C%20"
                "&location=" + Linkedinbot.adapt_words(job_search_specifics["city"]) + "%2C%20" +
                Linkedinbot.adapt_words(job_search_specifics["region"]) + "%2C%20" +
                Linkedinbot.adapt_words(job_search_specifics["country"])
            )
        else:
            job_list_url = (
                LINKEDIN_URL + "/jobs/search/?" +
                "&keywords=" + Linkedinbot.adapt_words(job_search_specifics["position"]) + "%2C%20"
                "&location=" + Linkedinbot.adapt_words(job_search_specifics["city"]) + "%2C%20" +
                Linkedinbot.adapt_words(job_search_specifics["region"]) + "%2C%20" +
                Linkedinbot.adapt_words(job_search_specifics["country"])
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
            Linkedinbot.sleep()

    def get_jobid_texts(self, jobs_id):

        jobs_data = []

        for job_id in jobs_id:

            job_data = {}
            try:
                job_data["id"] = job_id
                self.driver.get(Linkedinbot.get_one_job_url(job_id))
                Linkedinbot.sleep()
                src = self.driver.page_source.encode("utf-8")
                soup = BeautifulSoup(src, "lxml")
                try:
                    general_data = soup.find("div", {"class":"mt6"}).getText()
                    general_data = " ".join(re.findall('\\w+', general_data))
                except:
                    print(job_id, " has no general_data")
                try:
                    job_data["position"] = re.search(
                        '(.*)Company Name', general_data).group(1)
                except:
                    print(job_id, " has no position")
                try:
                    job_data["company_name"] = re.search(
                        'Company Name(.*)Company Location', general_data).group(1)
                except:
                    print(job_id, " has no company name")
                try:
                    job_data["location"] = re.search(
                        'Company Location(.*)Posted Date', general_data).group(1)
                except:
                    print(job_id, " has location")
                try:
                    job_data["posted_date"] = re.search(
                        'Posted Date Posted(.*)ago Number of applicants', general_data).group(1)
                except:
                    print(job_id, " has no posted date")
                try:
                    job_data["applicants"] = re.search(
                        'Number of applicants(.*)applicants', general_data).group(1)
                except:
                    print(job_id, " has no applicants")
                try:
                    job_details = soup.find("div", {"class":"jobs-description__details"}).getText()
                    job_details = " ".join(re.findall('\\w+', job_details))
                except:
                    print(job_id, " has no jobs_details")
                try:
                    job_data["level"] = re.search(
                        'Level(.*)Industry', job_details).group(1)
                except:
                    print(job_id, " has no level")
                try:
                    job_data["industry"] = re.search(
                        'Industry(.*)Employment Type', job_details).group(1)
                except:
                    print(job_id, " has no industry")
                try:
                    job_data["type"] = re.search(
                        'Employment Type(.*)Job Functions', job_details).group(1)
                except:
                    print(job_id, " has no type")
                try:
                    job_data["functions"] = re.search(
                        'Job Functions(.*)', job_details).group(1)
                except:
                    print(job_id, " has no functions")
                try:
                    text = soup.find("div", {"id":"job-details"}).getText()
                    text = re.sub("\n", " ", text)
                    job_data["text"] = text
                except:
                    print(job_id, " has no text")
                jobs_data.append(job_data)
            except WebDriverException:
                print(job_id, " failed to connect to job site")

        print(jobs_data)

        return jobs_data

    @staticmethod
    def get_one_job_url(job_id):

        job_url = LINKEDIN_URL + "/jobs/view/" + job_id

        return job_url

    @staticmethod
    def get_hours(name):

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

    @staticmethod
    def check_repeated_elements(jobs_to_check) -> None:

        repeated_elements = [
            job for job, count in collections.Counter(jobs_to_check).items() if count > 1]
        print("repeated_elements", repeated_elements)

    @staticmethod
    def create_jobs_data_file(jobs_data, file_name):

        performace_day = datetime.now().strftime("%Y-%m-%d")
        file_csv = "jobs_data" + "_" + file_name + "_" + performace_day + ".csv"
        csv_columns = jobs_data[0].keys()
        with open(file_csv, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in jobs_data:
                writer.writerow(data)

    @staticmethod
    def create_jobs_id_file(jobs_id, file_name):

        jobs_id = ",".join(jobs_id)
        performace_day = datetime.now().strftime("%Y-%m-%d")
        file_csv = "jobs_id" + "_" + file_name + "_" + performace_day + ".csv"
        with open(file_csv, 'w') as csvfile:
            wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            wr.writerow(jobs_id)
