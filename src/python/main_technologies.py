import itertools
from pymongo import MongoClient
import pandas as pd
import numpy as np
from neo4j_db import Neo4jConnector


DB_URL = ("mongodb+srv://jobs:f4Uo1b3ziIAhpPMf@cluster0-79fk" +
          "x.mongodb.net/jobs?retryWrites=true&w=majority")
DATA_BASE = "jobs"
COLLECTION = "datasciences_analysis"
URI = 'bolt://localhost:7687'
USER = "neo4j"
PASSWORD = "python"


def create_graph(data_base, neo4j):

    data_set = create_dataset(data_base)
    number_of_elements = data_set.shape[0]
    corr_matrix = get_corr_matrix(data_set)
    insert_nodes(neo4j, corr_matrix)
    insert_relationships(neo4j, corr_matrix, number_of_elements)


def create_dataset(data_base):

    jobs = list(data_base[COLLECTION].find({}))
    data_analyzed = pd.DataFrame(jobs)
    data_analyzed = data_analyzed[["job_id", "key_words"]]
    cluster_data = pd.DataFrame(columns=["job_id", "key_word"])
    shape = data_analyzed.shape[0]
    for i in range(0, shape):
        try:
            words = data_analyzed.key_words[i].split(" ")
            job_id = [data_analyzed.job_id[i]]*len(words)
            xtra = {"job_id": job_id, "key_word": words}
            cluster_data = cluster_data.append(pd.DataFrame(xtra))
        except: # pylint: disable=bare-except
            pass
    cluster_data["value"] = 1
    data_set = cluster_data.pivot_table(
        index="job_id", columns="key_word", values="value", fill_value=0)
    data_set = data_set.drop(columns=[""])

    return data_set


def get_corr_matrix(data_set):

    return data_set.corr(method=create_histogram_intersection)


def create_histogram_intersection(first_value, second_value):

    minimum = np.minimum(first_value, second_value).sum().round(decimals=1)

    return minimum


def insert_nodes(neo4j, corr_matrix):

    list(map(neo4j.insert_program, corr_matrix.columns))


def insert_relationships(neo4j, corr_matrix, number_of_elements):

    pair_elements = list(itertools.combinations(corr_matrix.columns, 2))
    list(
        map(lambda x: neo4j.insert_share_relationship(
            x[0], x[1],
            corr_matrix.loc[x[0], x[1]]/number_of_elements), pair_elements))


if __name__ == "__main__":

    DB = MongoClient(DB_URL).get_database(DATA_BASE)
    NEO4J = Neo4jConnector(URI, USER, PASSWORD)
    create_graph(DB, NEO4J)
