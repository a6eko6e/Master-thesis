from py2neo import Graph
import os

def connect_neo4j(uri=None, user=None, password=None):
    uri = uri or os.getenv("NEO4J_URI", "neo4juri")
    user = user or os.getenv("NEO4J_USER", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD", "password")
    try:
        graph = Graph(uri, auth=(user, password))
        print("Neo4j に正常に接続できました。")
        return graph
    except Exception as e:
        print(f"Neo4j接続に失敗しました: {e}")
        return None

# グローバルなGraphオブジェクト
graph = connect_neo4j()
