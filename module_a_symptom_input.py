from module_e_openai import get_text_embedding
from module_f_neo4j import graph
import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return np.dot(vec1, vec2) / (norm1 * norm2)

def find_most_similar_word(user_embedding, threshold=0.3):
    if user_embedding is None:
        return "ユーザーの埋め込みに当てはまる症状がないのでスキップします"

    query = """
    MATCH (s:Symptom)
    RETURN s.Name AS Name, s.embedding AS embedding
    """
    words = graph.run(query).data()
    if not words:
        return "データベースに症状が見つかりませんでした。"

    similarity_list = []

    for word in words:
        word_embedding = word['embedding']
        if word_embedding is None:
            continue
        similarity = cosine_similarity(user_embedding, word_embedding)
        similarity_list.append((word['Name'], similarity))

    # 類似度を高い順にソート
    similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

    # 全ての類似度をコンソールに表示
    print("全ての類似度:")
    for name, sim in similarity_list:
        print(f"症状: {name}, 類似度: {sim:.4f}")

    # 最も類似度が高い症状を返す
    if similarity_list:
        most_similar = similarity_list[0][0]
        return most_similar
    else:
        return "似ている症状が見つかりませんでした。"

def process_symptom(user_input, display_output):
    embedding = get_text_embedding(user_input)
    if embedding is None:
        print("ユーザーの埋め込みが生成できませんでした。")
    return embedding
