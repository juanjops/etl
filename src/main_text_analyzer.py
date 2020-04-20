from datetime import datetime
import csv
import os
from text_analyzer import JobsWords
from os import listdir
from os.path import isfile, join


DATA_BASE_ETL_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\etl\\"
DATA_BASE_TEXT_ROUTE = "C:\\Users\\Sectorea\\Code\\database_linkedin\\text_analyzed\\"

# FILE = "data_science_New_Zealand_Any_Time_2020-04-17.csv"
all_files = [file for file in listdir(DATA_BASE_ETL_ROUTE) if isfile(join(DATA_BASE_ETL_ROUTE, file))]
files_already_analyzed = [
    file.split("text_analyze_",1)[1] for file in listdir(DATA_BASE_TEXT_ROUTE)
    if isfile(join(DATA_BASE_TEXT_ROUTE, file))]
new_files = [
    file for file in listdir(DATA_BASE_ETL_ROUTE)
    if isfile(join(DATA_BASE_ETL_ROUTE, file)) and 
    (file not in files_already_analyzed)]

KEY_WORDS_PARTS = {
    "languages": [
        "python", "r", "scala", "matlab", "java", "kotlin", "javascript", "node",
        "clojure"],
    "data_base": [
        "impala", "spark", "hive", "kudu", "sql", "no sql", "kafka", "hadoop",
        "sqoop", "mongo", "flume", "nifi", "ssas", "hdfs", "postgresql", "elasticsearch",
        "postgre", "pyspark", "lucene", "redis", "kinesis"],
    "bi": [
        "qlik", "tableau", "powerbi", "qlikview", "qliksense", "kibana"],
    "blockchain": [
        "neo", "blockchain"],
    "companies": [
        "ab initio", "cloudera", "google", "databricks", "knime", "qubole"],
    "data_parts": [
        " api", "etl", "b2b", "agile", "kpi", "crm", "scrum", "mining", "dashboard",
        "visualisation", "startup", " bi", "backend", "frontend",
        "virtualization", "micromanagement", "mathematic", "microservice"],
    "cloud": [
        "aws", "gcp", "cloud", "azure"],
    "machine_learning": [
        "ai", "nlp"],
    "libraries": [
        "tensorflow", "keras", "sklearn", "redux", "pytorch", "jupyter"],
    "microservices": [
        "docker", "kubernetes", "ansible", "jenkins", "kubeflow", "sagemaker"
    ],
    "operative_system": [
        "linux", "windows"
    ],
    "development": [
        "gitlab", "github", "jira", "confluence", "angular", "bitbucket"
    ]
}

KEY_WORDS = sum(KEY_WORDS_PARTS.values(), [])


def get_jobs_data(file_name):

    file_data = []
    with open(DATA_BASE_ETL_ROUTE + file_name, encoding='utf-8') as file_to_read:
        read_file = csv.DictReader(file_to_read, delimiter=',')
        for row in read_file:
            file_data.append(dict(row))

    return file_data


def get_text_analyzed(jobs_data, key_words):

    for job in jobs_data:

        try:
            jobs_token_text = JobsWords(job["text"], key_words)
            job["key_words"], job["misspelled_words"], job["Experience"] = \
                 jobs_token_text.get_key_misspelled_words()
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

    # JOBS_DATA = get_jobs_data(FILE)

    # JOBS_DATA_ANALYZED = get_text_analyzed(JOBS_DATA, KEY_WORDS)

    # get_csv_from_list_of_dicts(JOBS_DATA_ANALYZED, FILE)

    for file in new_files:

        JOBS_DATA = get_jobs_data(file)

        JOBS_DATA_ANALYZED = get_text_analyzed(JOBS_DATA, KEY_WORDS)

        get_csv_from_list_of_dicts(JOBS_DATA_ANALYZED, file)
