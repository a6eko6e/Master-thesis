from module_f_neo4j import graph

def find_level2_category(symptom, display_output):
    if symptom is None:
        display_output("症状がありません")
        return []
    
    query = """
    MATCH (s3:Symptom {Name: $symptom_name})<-[:HAS_SYMPTOM]-(s2:Symptom_Type)
    OPTIONAL MATCH (s2)<-[:PARENT]-(parent:Symptom_Type)
    RETURN s2.Name AS category,
           parent.Name AS parent_category
    """
    result = graph.run(query, symptom_name=symptom).data()

    if not result:
        display_output("関連する状態像が見つかりませんでした。")
        return []

    # 全カテゴリのログ表示（親子関係を無視）
    all_categories = {row["category"] for row in result}

    categories = []
    parent_child_mapping = {}

    for row in result:
        category = row["category"]
        parent_category = row["parent_category"]

        if parent_category:
            if parent_category not in parent_child_mapping:
                parent_child_mapping[parent_category] = []
            parent_child_mapping[parent_category].append(category)
        else:
            if category not in categories:
                categories.append(category)

    # 親カテゴリ優先でリストを構築
    for parent, children in parent_child_mapping.items():
        if parent in categories:
            continue
        categories.append(parent)
        for child in children:
            if child not in categories:
                categories.append(child)

    display_output(f"検索された状態像: {', '.join(categories)}")
    return categories

def ask_category_questions(categories, current_score, most_similar, display_output, ask_user):
    if not categories:
        return current_score

    all_questions = []

    # 種類Aの質問を取得（必ず実行）
    for category in categories:
        query_questions_a = """
        MATCH (cat:Symptom_Type {Name: $category_name})-[:QUESTIONLIST]->(q:Question)
        MATCH (q)-[:ANSWER]->(s:Severe_symptom)<-[:HAS_SEVERESYMPTOM]-(cat)
        RETURN q.question_id AS question_id, q.Text AS question_text
        """
        question_nodes_a = graph.run(query_questions_a, category_name=category).data()
        all_questions.extend(question_nodes_a)

    # 種類Bの質問を取得（most_similar と一致する Symptom のみ実行）
    if most_similar:
        query_questions_b = """
        MATCH (sym:Symptom {Name: $most_similar})-[:HAS_SEVERESYMPTOM]->(s:Severe_symptom)
        MATCH (q:Question)-[:ANSWER]->(s)
        RETURN q.question_id AS question_id, q.Text AS question_text
        """
        question_nodes_b = graph.run(query_questions_b, most_similar=most_similar).data()
        all_questions.extend(question_nodes_b)

    # 質問の重複を排除
    unique_questions = {row['question_text']: row for row in all_questions}.values()

    asked_questions = set()
    for question in unique_questions:
        question_text = question["question_text"]
        question_id = question["question_id"]

        if question_text in asked_questions:
            continue  # 重複質問はスキップ
        asked_questions.add(question_text)

        display_output(f"質問: {question_text}")
        while True:
            user_answer = ask_user("yes/noで答えてください: ").lower()
            if user_answer in ['yes', 'no']:
                break
            else:
                display_output("無効な入力です。「yes」または「no」で答えてください。")

        # スコアの計算
        query_score = """
        MATCH (s:Severe_symptom)
        WHERE s.question_id = $question_id
        RETURN s.Name AS Name, s.severe_score AS severe_score
        """
        result = graph.run(query_score, question_id=question_id).data()
        if result:
            Name = result[0]["Name"]
            severe_score = result[0]["severe_score"]
            if user_answer == 'yes':
                if current_score == 0:
                    current_score += severe_score
                    display_output(f"カテゴリスコアが{severe_score}に更新されました。")
                else:
                    display_output(f"現在のスコアは{current_score}です。スコアは変わりません。")
                display_output(f"この症状は{Name}です。またこの重症度スコアは{severe_score}です")
            else:
                display_output(f"スコアは変わりません。")
            display_output(f"現在のカテゴリ質問によるスコア: {current_score}")
        else:
            display_output(f"質問ID {question_id} に対応するスコアが見つかりませんでした。")

    return current_score
