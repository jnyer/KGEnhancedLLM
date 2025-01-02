import json
from neo4j import GraphDatabase

class Neo4jBatchCreator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_nodes_and_relationships(self, universities, locations, is_located_in):
        with self.driver.session() as session:
            # 创建节点
            for university in universities:
                session.run(
                    "MERGE (u:University {name: $name}) ",
                    name=university['name']
                )
            
            # 创建节点
            for location in locations:
                session.run(
                    "MERGE (l:Location {name: $name}) ",
                    name=location['name']
                )
            
            # 创建 is_located_in 关系
            for located in is_located_in:
                session.run(
                    "MATCH (u:University {name: $university}), (l:Location {name: $location}) "
                    "MERGE (u)-[r:is_located_in]->(l) ",
                    university=located['university'], location=located['location']
                )

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "12345678"

    creator = Neo4jBatchCreator(uri, user, password)

    with open('universities.json', 'r', encoding='utf-8') as f:
        universities = json.load(f)

    with open('locations.json', 'r', encoding='utf-8') as f:
        locations = json.load(f)

    with open('output.json', 'r', encoding='utf-8') as f:
        is_located_in = json.load(f)

    creator.create_nodes_and_relationships(universities, locations, is_located_in)
    creator.close()
