from datetime import datetime
import csv
from random import uniform
import time
from bot import BotJobsId, BotJobsData


USER = "juanjose.pardo.s@gmail.com"

PASSWORD = "malekith1990"

DATA_BASE_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\etl\\"

JOB_SEARCH_SPECS = {
    "key_words": "data science",
    "location" : "london",
    "time_range": "Past 24 hours"
}

DRIVER = "Chrome"

TIME_SLEEP_GAP = [120, 240]


def get_csv_from_list_of_dicts(one_jobs_data, job_search_specs):

    file_csv = "_".join([
        job_search_specs["position"], job_search_specs["location"],
        job_search_specs["time_range"]])
    file_csv = file_csv.replace(" ", "_")
    performance_day = datetime.now().strftime("%Y-%m-%d")
    file_csv = DATA_BASE_ROUTE + file_csv + "_" + performance_day + ".csv"
    csv_columns = one_jobs_data[0].keys()

    with open(file_csv, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in one_jobs_data:
            writer.writerow(data)


if __name__ == "__main__":

    BOT_JOBS_ID = BotJobsId(DRIVER, USER, PASSWORD)
    JOBS_ID = BOT_JOBS_ID.get_jobs_id(JOB_SEARCH_SPECS)
    BOT_JOBS_ID.close_driver()

    time.sleep(uniform(TIME_SLEEP_GAP[0], TIME_SLEEP_GAP[1]))

    BOT_JOBS_DATA = BotJobsData(DRIVER)
    JOBS_DATA = BOT_JOBS_DATA.get_jobs_data(JOBS_ID)
    get_csv_from_list_of_dicts(JOBS_DATA, JOB_SEARCH_SPECS)
    BOT_JOBS_DATA.close_driver()
