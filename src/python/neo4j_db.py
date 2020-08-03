from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self, uri, user, password):

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):

        self.driver.close()

    def insert_program(self, program):

        with self.driver.session() as session:

            session.write_transaction(self._create_query_program, program)

    @staticmethod
    def _create_query_program(transfer, program):

        transfer.run(
            "MERGE (program:Program {name: $program}) "
            "RETURN program", program=program)

    def insert_job(self, job):

        with self.driver.session() as session:

            session.write_transaction(self._create_query_job, job)

    @staticmethod
    def _create_query_job(transfer, job):

        transfer.run(
            "MERGE (job:Job {name: $job}) "
            "RETURN job", job=job)

    def insert_word(self, word):

        with self.driver.session() as session:

            session.write_transaction(self._create_query_word, word)

    @staticmethod
    def _create_query_word(transfer, word):

        transfer.run(
            "MERGE (word:Word {name: $word}) "
            "RETURN word", word=word)

    def insert_share_relationship(self, program_a, program_b, weight):

        with self.driver.session() as session:

            session.write_transaction(self._create_program_relationship, program_a, program_b, weight)

    @staticmethod
    def _create_program_relationship(transfer, program_a, program_b, weight):

        transfer.run(
            "MATCH (a:Program{name: $program_a}), (b:Program{name: $program_b}) "
            "MERGE (a)-[:SHARE {weight: $weight}]->(b) "
            "RETURN a, b ", program_a=program_a, program_b=program_b, weight=weight)

    def insert_job_relationship(self, job, program):

        with self.driver.session() as session:

            session.write_transaction(self._create_job_relationship, job, program)

    @staticmethod
    def _create_job_relationship(transfer, job, program):

        transfer.run(
            "MATCH (a:Program{name: $job}), (b:Program{name: $program}) "
            "MERGE (a)-[:SHARE {weight: $weight}]->(b) "
            "RETURN a, b ", job=job, program=program)

    def insert_job_word_relationship(self, job, word):

        with self.driver.session() as session:

            session.write_transaction(self._create_job_word_relationship, job, word)

    @staticmethod
    def _create_job_word_relationship(transfer, job, word):

        transfer.run(
            "MATCH (a:Job{name: $job}), (b:Word{name: $word}) "
            "MERGE (a)-[:CONTAINS]->(b) "
            "RETURN a, b ", job=job, word=word)