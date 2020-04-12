from datetime import datetime
import csv
from bot import bot_jobs_id, bot_jobs_data


USER = "juanjose.pardo.s@gmail.com"

PASSWORD = "malekith1990"

DATA_BASE_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\"

JOBS_LOCATIONS = [
    ["Madrid", "Community of Madrid", "Spain"]]

DRIVER = "Chrome"


def get_jobs_format_spec(job_location_specs):

    job_locations_specs = {
        "position": "data scientist",
        "city": job_location_specs[0],
        "region": job_location_specs[1],
        "country": job_location_specs[2],
        "time_range": "Past Week"
    }

    return job_locations_specs


def get_csv_from_list_of_dicts(one_jobs_data, job_search_specs):

    file_csv = "_".join([
        job_search_specs["position"], job_search_specs["city"],
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

    BOT_JOBS_ID = bot_jobs_id(DRIVER, USER, PASSWORD)

    BOT_JOBS_DATA = bot_jobs_data(DRIVER)

    for job_specs in JOBS_LOCATIONS:

        job_specs = get_jobs_format_spec(job_specs)

        jobs_id = BOT_JOBS_ID.get_jobs_id(job_specs)

        jobs_data = BOT_JOBS_DATA.get_jobs_data(jobs_id)

        get_csv_from_list_of_dicts(jobs_data, job_specs)

    BOT_JOBS_ID.close_driver()

    BOT_JOBS_DATA.close_driver()
