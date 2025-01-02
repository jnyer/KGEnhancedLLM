from neo4j import GraphDatabase
import json

# 1. 连接配置
# --------------------------------------------------------------------------------
NEO4J_URI = "bolt://localhost:7687"   # 本地测试地址，若是远程数据库，请改为实际地址
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

# 2. 示例 JSON 数据
# --------------------------------------------------------------------------------
# 方式1：直接在脚本中定义一个列表
# json_data = [
#     {"id": 1, "title": "Engineer"},
#     {"id": 2, "title": "Manager"}
# ]

# 方式2：从本地文件读取 JSON
with open("output2.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 3. 建立驱动和会话
# --------------------------------------------------------------------------------
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 4. 更新函数
# --------------------------------------------------------------------------------
def update_university_level(data_list):
    """
    使用 UNWIND 批量更新 :University 节点的 level 属性。
    data_list 是一个包含 {id: ..., title: ...} 的列表
    """
    query = """
    UNWIND $data AS row
    MATCH (u:University {name: row.university})
    SET u.level = row.level
    RETURN u
    """

    # 如果你想做 “如果不存在则创建，否则更新”，可使用 MERGE/ON CREATE/ON MATCH：
    # query = """
    # UNWIND $data AS row
    # MERGE (p:Person {id: row.id})
    # ON CREATE SET p.title = row.title, p.createdAt = timestamp()
    # ON MATCH  SET p.title = row.title, p.updatedAt = timestamp()
    # RETURN p
    # """

    with driver.session() as session:
        result = session.run(query, data=data_list)
        # 遍历返回结果（可选）
        for record in result:
            updated_node = record["u"]
            print(f"Updated University node -> id: {updated_node.get('name')}, level: {updated_node.get('level')}")

# 5. 主执行逻辑
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        update_university_level(json_data)
    finally:
        # 关闭 driver
        driver.close()