from pymongo import MongoClient
import en_core_web_sm
import es_core_news_sm
from neo4j_db import Neo4jConnector
from text_analyzer import JobsWords


DB_URL = ("mongodb+srv://jobs:f4Uo1b3ziIAhpPMf@cluster0-79fk" +
          "x.mongodb.net/jobs?retryWrites=true&w=majority")
DATA_BASE = "jobs"
COLLECTION = "datasciences"
URI = 'bolt://localhost:7687'
USER = "neo4j"
PASSWORD = "jobs"
EN_NLP = en_core_web_sm.load()
ES_NLP = es_core_news_sm.load()
MODELS = {
    "en": EN_NLP,
    "es": ES_NLP
}


TEXT_ANALYZER = JobsWords("-", MODELS)


def create_graph(data_base, neo4j):

    data_set = create_dataset(data_base)
    jobs_tokens = {
        job_id: get_tokens(job_text) for job_id, job_text
        in data_set.items() if job_text is not None}
    insert_jobs(neo4j, jobs_tokens)
    insert_words(neo4j, jobs_tokens)
    insert_relationships(neo4j, jobs_tokens)


def create_dataset(data_base):

    jobs = list(data_base[COLLECTION].find(
        {}, {"job_id":1, "text":1}))
    data_set = {job["job_id"]: job["text"] for job in jobs}

    return data_set


def get_tokens(text):

    try:
        language = TEXT_ANALYZER.get_language(text)
        clean_text = TEXT_ANALYZER.get_reg(text)
        tokens = TEXT_ANALYZER.get_tokens(language, clean_text)
    except: # pylint: disable=bare-except
        tokens = None

    return tokens


def insert_jobs(neo4j, jobs_tokens):

    list(map(neo4j.insert_job, jobs_tokens.keys()))


def insert_words(neo4j, jobs_tokens):

    tokens = list(dict.fromkeys(sum(jobs_tokens.values(), [])))
    list(map(neo4j.insert_word, tokens))


def insert_relationships(neo4j, jobs_tokens):

    for job_id, tokens in jobs_tokens.items():

        list(map(lambda token, job=job_id: neo4j.insert_job_word_relationship(job, token), tokens))


if __name__ == "__main__":

    DB = MongoClient(DB_URL).get_database(DATA_BASE)
    NEO4J = Neo4jConnector(URI, USER, PASSWORD)
    create_graph(DB, NEO4J)
