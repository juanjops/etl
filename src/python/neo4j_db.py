from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self, uri, user, password):

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):

        self.driver.close()

    def insert_user(self, user):

        with self.driver.session() as session:

            session.write_transaction(self._create_query_user, user)

    @staticmethod
    def _create_query_user(transfer, user):

        transfer.run(
            "MERGE (program:Program {name: $user}) "
            "RETURN program", user=user)

    def insert_relationship(self, user, following, weight):

        with self.driver.session() as session:

            session.write_transaction(self._create_query_relationship, user, following, weight)

    @staticmethod
    def _create_query_relationship(transfer, user, following, weight):

        transfer.run(
            "MATCH (a:Program{name: $user}), (b:Program{name: $following}) "
            "MERGE (a)-[:SHARE {weight: $weight}]->(b) "
            "RETURN a, b ", user=user, following=following, weight=weight)
