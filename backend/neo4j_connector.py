from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query):
        with self.driver.session() as session:
            return session.run(query).data()

db = Neo4jConnection(
    uri="neo4j+s://80693212.databases.neo4j.io",  # Use your AuraDB URI
    user="neo4j",
    password="2NB6LSyOCRZgWKn7_tSMFLWu2lz0UEoJ0CZEBXswmFc"  # Replace with actual password you use to login to Aura
)
results = db.query("MATCH (n)-[r]->(m) RETURN n.name AS from, TYPE(r) AS rel, m.name AS to")
print(results)
db.close()


