import json
from neo4j import GraphDatabase

# 1. 连接 Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

def import_json_data(json_file_path):
    # 2. 读取本地 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    # 3. 构建要执行的 Cypher 语句
    #    - UNWIND 将 JSON 数组元素依次展开为 row
    #    - MATCH (e:Existing { id: row.relatedExistingId }) 去匹配已有节点
    #    - CREATE (n:NewLabel { ... }) 创建新节点
    #    - CREATE (n)-[:RELATED_TO]->(e) 建立关系
    cypher_query = """
    UNWIND $jsonList AS row
    MATCH (u:University { name: "哈尔滨工业大学" })
    CREATE (c:College { name: row.name })
    CREATE (c)-[:belongs_to]->(u)
    """

    # 如果不确定已有节点是否一定存在，也可以改用 MERGE 或者 ON CREATE / ON MATCH 等逻辑

    # 4. 执行语句
    with driver.session() as session:
        result = session.run(cypher_query, jsonList=data_list)
        summary = result.consume()
        print("Nodes created:", summary.counters.nodes_created)
        print("Relationships created:", summary.counters.relationships_created)

if __name__ == "__main__":
    import_json_data("colleges_university.json")
    driver.close()
