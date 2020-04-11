from datetime import datetime
import csv
from bot import Linkedinbot
from text_analyzer import JobsWords


# JOB_SEARCH_SPECS = {
#     "position": "data scientist",
#     "city": "Madrid",
#     "region": "Community of Madrid",
#     "country": "Spain",
#     "time_range": "Past Month"
# }

JOB_SEARCH_SPECS = {
    "position": "data scientist",
    "city": "London",
    "region": "England",
    "country": "United Kingdom",
    "time_range": "Past 24 hours"
}

KEY_WORDS = [
    "python", "r", "qlik", "tableau", "powerbi", "scala", "impala", "spark", "hive", "mathlab"
    "kudu", "sql", "kafka", "neo", "initio", "hadoop", "apis", "aws", "java",
    "gcp", "cloud", "azure", "sqoop", "etl", "cloudera", "b2b", "b2c", "agile", "kpi", "crm",
    "scrum", "tensorflow", "keras", "sklearn", "docker", "mining", "no-sql", "mongo"
]

DRIVER = "Chrome"
LANGUAGES = ["en", "es"]


def get_etl_file_name():

    job_file = "_".join(
        [JOB_SEARCH_SPECS["position"], JOB_SEARCH_SPECS["city"],
         JOB_SEARCH_SPECS["time_range"]
        ])
    job_file = job_file.replace(" ", "_")

    return job_file

def get_text_analized_file_name():

    job_file = "text_analyzed" + "_" + "_".join(
        [JOB_SEARCH_SPECS["position"], JOB_SEARCH_SPECS["city"],
         JOB_SEARCH_SPECS["time_range"]
        ])
    job_file = job_file.replace(" ", "_")

    return job_file


def get_csv_from_dict(jobs_data, file_name):

    performace_day = datetime.now().strftime("%Y-%m-%d")
    file_csv = file_name + "_" + performace_day + ".csv"
    csv_columns = jobs_data[0].keys()
    with open(file_csv, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in jobs_data:
            writer.writerow(data)


def get_text_analyzed(jobs_data, key_words, languages) -> None:

    for job in jobs_data:

        try:
            jobs_token_text = JobsWords(job["text"], key_words, languages)
            job["key_words"], job["misspelled_words"] = \
                 jobs_token_text.get_key_misspelled_words()
            del job["text"]
        except:
            print(job["id"], " no text analyzed")

    return jobs_data


if __name__ == "__main__":

    LINKEDIN_BOT = Linkedinbot(DRIVER)

    JOBS_DATA = LINKEDIN_BOT.get_jobs_data(JOB_SEARCH_SPECS)

    get_csv_from_dict(JOBS_DATA, get_etl_file_name())

    JOBS_DATA_ANALYZED = get_text_analyzed(JOBS_DATA, KEY_WORDS, LANGUAGES)

    get_csv_from_dict(JOBS_DATA_ANALYZED, get_text_analized_file_name())
