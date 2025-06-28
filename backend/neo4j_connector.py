import os
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASS")
        if not all([self.uri, self.user, self.password]):
            raise ValueError("NEO4J credentials not set in environment variables.")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def query(self, query):
        with self.driver.session() as session:
            return session.run(query).data()
