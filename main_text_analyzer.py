from datetime import datetime
import csv
import os
from text_analyzer import JobsWords


DATA_BASE_ETL_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\etl"

DATA_BASE_TEXT_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\text_analyzed"

KEY_WORDS = [
    "python", "r", "qlik", "tableau", "powerbi", "scala", "impala", "spark", "hive", "mathlab"
    "kudu", "sql", "kafka", "neo", "initio", "hadoop", "apis", "aws", "java",
    "gcp", "cloud", "azure", "sqoop", "etl", "cloudera", "b2b", "b2c", "agile", "kpi", "crm",
    "scrum", "tensorflow", "keras", "sklearn", "docker", "mining", "no-sql", "mongo", 
    "dashboards", "analytics", "visualisations", "kpis", "kubernetes", "startups"
]

LANGUAGES = ["en", "es"]


def get_csvs_to_analyze():

    all_files = os.listdir(DATA_BASE_ETL_ROUTE)
    today = datetime.today().strftime("%Y-%m-%d")
    files = [
        file for file in all_files if (
            (file.split("_")[-1].split(".")[0] == today) &
            (file.split("_")[0] != "text"))]

    return files


def get_jobs_data(file_name):

    file_data = []
    with open(DATA_BASE_ETL_ROUTE + file_name, encoding='utf-8') as file_to_read:
        read_file = csv.DictReader(file_to_read, delimiter=',')
        for row in read_file:
            file_data.append(dict(row))

    return file_data


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


def get_csv_from_list_of_dicts(one_jobs_data, file_name):

    file_csv = DATA_BASE_TEXT_ROUTE + "text_analyze_" + file_name
    csv_columns = one_jobs_data[0].keys()

    with open(file_csv, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in one_jobs_data:
            writer.writerow(data)


if __name__ == "__main__":

    FILES = get_csvs_to_analyze()

    for file in FILES:

        JOBS_DATA = get_jobs_data(file)

        JOBS_DATA_ANALYZED = get_text_analyzed(JOBS_DATA, KEY_WORDS, LANGUAGES)

        get_csv_from_list_of_dicts(JOBS_DATA_ANALYZED, file)
