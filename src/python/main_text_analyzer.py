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
COLLECTION = "datasciences"
ANALYSYS_COLLECTION = COLLECTION + "_analysis"
EN_NLP = en_core_web_sm.load()
ES_NLP = es_core_news_sm.load()
MODELS = {
    "en": EN_NLP,
    "es": ES_NLP
}

KEY_WORDS = {
    "ML": [
        "python", "r", "tensorflow", "keras", "sklearn", "pytorch", "jupyter", "nlp"
    ],
    "Math": [
        "matlab", "ai", "mathematic"
    ],
    "BI": [
        "sql", "no sql", "qlik", "tableau", "powerbi", "qlikview", "qliksense", "kibana", "dashboard",
        "visualisation", "bi"
    ],
    "Big_D": [
        "scala", "impala", "spark", "hive", "kudu", "kafka", "hadoop", "sqoop", "mongo", "flume", "nifi", "ssas", "hdfs",
        "postgre", "pyspark", "lucene", "redis", "kinesis"
    ],
    "CI_CD": [
        "ab initio", "cloudera", "gcp", "databricks", "knime", "qubole", "b2b", "agile", "aws", "azure", 
        "gitlab", "github", "jira", "confluence", "angular", "bitbucket"
    ],
    "Serv": [
        "java", "kotlin", "javascript", "node", "clojure", "neo", "blockchain", " api", "etl", "kpi", "crm",
        "backend", "frontend", "virtualization", "micromanagement", "docker", "kubernetes", "ansible", "jenkins",
        "kubeflow", "sagemaker", "redux"
    ]
}

TEXT_ANALYZER = JobsWords(KEY_WORDS, MODELS)


def create_analysis(db):

    print("start time: ", datetime.datetime.now())
    delete_repeated_jobs(db, COLLECTION)
    print("raw collection jobs: ", db[COLLECTION].count_documents({}))
    jobs_id = [job["job_id"] for job in list(
        db[COLLECTION].find({}, {"job_id":1}))] 
    jobs_id_already_analyzed = [job["job_id"] for job in list(
        db[ANALYSYS_COLLECTION].find({}, {"job_id":1}))]
    print("jobs already analyzed: ", len(jobs_id_already_analyzed))
    jobs_id_not_analyzed = [job_id for job_id in jobs_id if job_id not in jobs_id_already_analyzed]
    print("jobs to analyzed: ", len(jobs_id_not_analyzed))
    jobs = list(db[COLLECTION].find(
        {"job_id" : {"$in" : jobs_id_not_analyzed}}, {"job_id":1, "text":1, "available":1}))
    for job in jobs:
        get_job_analysis(job)
        db[ANALYSYS_COLLECTION].insert_one(job)
    print("finish time: ", datetime.datetime.now())


def delete_repeated_jobs(db, collection):

    db[collection].aggregate(	
    [ 	
        { "$sort": { "_id": 1 } }, 	
        { "$group": { 	
            "_id": "$job_id", 	
            "doc": { "$first": "$$ROOT" } 	
        }}, 	
        { "$replaceRoot": { "newRoot": "$doc" } },	
        { "$out": "auxiliar_collection"}	
    ])

    db[collection].drop()
    db["auxiliar_collection"].rename(collection)


def get_job_analysis(job):
    try:
        text_analysis = TEXT_ANALYZER.get_key_misspelled_words(job["text"])
        job["key_words"] = text_analysis[0]
        job["misspelled_words"] = text_analysis[1]
        job["experience"] = text_analysis[2]
        job["ML"] = text_analysis[3]["ML"]
        job["Math"] = text_analysis[3]["Math"]
        job["BI"] = text_analysis[3]["BI"]
        job["Big_D"] = text_analysis[3]["Big_D"]
        job["CI_CD"] = text_analysis[3]["CI/CD"]
        job["Serv"] = text_analysis[3]["Serv"]
        job["language"] = text_analysis[4]
        del job["text"]
    except:
        job["key_words"] = None
        job["misspelled_words"] = None
        job["experience"] = None
        job["ML"] = None
        job["Math"] = None
        job["BI"] = None
        job["Big_D"] = None
        job["CI_CD"] = None
        job["Serv"] = None
        job["language"] = None


if __name__ == "__main__":

    DB = MongoClient(DB_URL).get_database(DATA_BASE)

    create_analysis(DB)
