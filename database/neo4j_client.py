from neo4j import GraphDatabase
from config.neo4j_config import NEO4J_CONFIG

class Neo4jClient:
    def __init__(self):
        self.uri = NEO4J_CONFIG["uri"]
        self.user = NEO4J_CONFIG["user"]
        self.password = NEO4J_CONFIG["password"]
        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        if self.driver:
            self.driver.close()

    def execute_query(self, cypher_query):
        if not self.driver:
            self.connect()
        with self.driver.session() as session:
            result = session.run(cypher_query)
            return [record.data() for record in result]

neo4j_client = Neo4jClient()