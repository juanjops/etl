from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import datetime
from text_analyzer import JobsWords
import json
import en_core_web_sm
import es_core_news_sm


DB_URL = 'mongodb+srv://jobs:f4Uo1b3ziIAhpPMf@cluster0-79fkx.mongodb.net/jobs?retryWrites=true&w=majority'
DATA_BASE = "jobs"
COLLECTION = "linkedins"
CLEAN_COLLECTION = COLLECTION + "_clean"
ANALYSYS_COLLECTION = COLLECTION + "_analysis"
EN_NLP = en_core_web_sm.load()
ES_NLP = es_core_news_sm.load()
MODELS = {
    "en": EN_NLP,
    "es": ES_NLP
}

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

TEXT_ANALYZER = JobsWords(KEY_WORDS, MODELS)

def get_key_words(job):
    try:
        job["tokens"] = TEXT_ANALYZER.get_key_misspelled_words(job["text"])[0]
        job["key_words"] = TEXT_ANALYZER.get_key_misspelled_words(job["text"])[1]
        job["misspelled_words"] = TEXT_ANALYZER.get_key_misspelled_words(job["text"])[2]
        job["experience"] = TEXT_ANALYZER.get_key_misspelled_words(job["text"])[3]
        del job["text"]
    except:
        job["tokens"] = None
        job["key_words"] = None
        job["misspelled_words"] = None
        job["experience"] = None


def create_analysis(db):

    print("start time: ", datetime.datetime.now())
    print("raw collection jobs: ", db[COLLECTION].count_documents({}))
    jobs_id = [job["job_id"] for job in list(
        db[COLLECTION].find({}, {"job_id":1}))] 
    jobs_id_already_analyzed = [job["job_id"] for job in list(
        db[ANALYSYS_COLLECTION].find({}, {"job_id":1}))]
    print("jobs already analyzed: ", len(jobs_id_already_analyzed))
    jobs_id_not_analyzed = [job_id for job_id in jobs_id if job_id not in jobs_id_already_analyzed]
    jobs_id_not_analyzed = list(dict.fromkeys(jobs_id_not_analyzed))
    jobs = list(db[COLLECTION].find(
        {"job_id" : {"$in" : jobs_id_not_analyzed}}, {"job_id":1, "text":1}))
    for job in jobs:
        get_key_words(job)
        db[ANALYSYS_COLLECTION].insert_one(job)
    print("finish time: ",datetime.datetime.now())


if __name__ == "__main__":

    DB = MongoClient(DB_URL).get_database(DATA_BASE)

    create_analysis(DB)
