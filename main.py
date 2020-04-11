from bot import Linkedinbot
from text_analyzer import JobsWords


USER = "xxxxxxxx"
PASSWORD = "xxxxxxx"

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
    "time_range": "Past Month"
}

KEY_WORDS = [
    "python", "r", "qlik", "tableau", "powerbi", "scala", "impala", "spark", "hive", "mathlab"
    "kudu", "sql", "kafka", "neo", "initio", "hadoop", "apis", "aws", "java",
    "gcp", "cloud", "azure", "sqoop", "etl", "cloudera", "b2b", "b2c", "agile", "kpi", "crm",
    "scrum", "tensorflow", "keras", "sklearn", "docker", "mining"
]

DRIVER = "Chrome"
LANGUAGES = ["en", "es"]


def get_process_file_name():

    job_file = "_".join(
        [JOB_SEARCH_SPECS["position"], JOB_SEARCH_SPECS["city"],
         JOB_SEARCH_SPECS["region"], JOB_SEARCH_SPECS["country"],
         JOB_SEARCH_SPECS["time_range"]
        ])
    job_file = job_file.replace(" ", "_")

    return job_file


def get_csv_jobs(jobs_data, key_words, languages) -> None:

    for job in jobs_data:

        try:
            jobs_token_text = JobsWords(job["text"], key_words, languages)
            job["key_words"], job["misspelled_words"] = \
                 jobs_token_text.get_key_misspelled_words()
            del job["text"]
        except:
            pass


if __name__ == "__main__":

    LINKEDIN_BOT = Linkedinbot(DRIVER, USER, PASSWORD)

    JOBS_DATA = LINKEDIN_BOT.get_jobs_data(JOB_SEARCH_SPECS, get_process_file_name())

    # get_csv_jobs(JOBS_DATA, KEY_WORDS, LANGUAGES)
