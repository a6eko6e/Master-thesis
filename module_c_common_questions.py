from module_f_neo4j import graph

def apply_special_rule(selected_option_name):
    query = """
    MATCH (c:Consult {Name: $option_name})-[:IS_A]->(u:Urgency)
    RETURN u.Name AS urgency_level
    """
    result = graph.run(query, option_name=selected_option_name).data()
    if result:
        return result[0]['urgency_level']
    return None

def ask_common_questions(display_output, ask_user):
    query_common = """
    MATCH (q:Question)
    WHERE q.question_type = "common"
    RETURN q.question_id AS question_id, q.Text AS question_text
    """
    try:
        question_list = graph.run(query_common).data()
        display_output(f"DEBUG: 共通質問を {len(question_list)} 件取得。")
    except Exception as e:
        display_output(f"DEBUG: 共通質問取得中にエラー: {e}")
        return 0, None

    commonscore = 0
    special_urgency = None  # 特別ルール適用結果を記録する

    for row in question_list:
        question_text = row["question_text"]
        question_id = row["question_id"]
        display_output(f"\n質問: {question_text}")
        
        query = """
        MATCH (s)
        WHERE ('Period' IN labels(s) OR 'Affect' IN labels(s) OR 'Consult' IN labels(s))
              AND s.question_id = $question_id
        RETURN s.Name AS option, s.severe_score AS severe_score
        """
        try:
            options = graph.run(query, question_id=question_id).data()
        except Exception as e:
            display_output(f"選択肢取得中にエラー: {e}")
            continue

        if not options:
            display_output(f"質問ID {question_id} に対応する選択肢が見つかりませんでした。")
            continue

        display_output(f"質問ID {question_id} に対する選択肢:")
        for idx, option in enumerate(options, 1):
            display_output(f"{idx}. {option['option']}")

        while True:
            user_answer_str = ask_user(f"1〜{len(options)} の番号を入力してください: ")
            try:
                user_answer = int(user_answer_str)
                if 1 <= user_answer <= len(options):
                    break
                else:
                    display_output("無効な選択肢です。")
            except ValueError:
                display_output("無効な入力です。数字を入力してください。")

        selected_option = options[user_answer - 1]
        selected_option_name = selected_option['option']

        # 特別ルールを確認
        if special_urgency is None:  # 特別ルール未適用の場合のみ確認
            special_urgency = apply_special_rule(selected_option_name)
            if special_urgency:
                display_output(f"特別ルールが適用されました: 緊急性は {special_urgency} です。")

        # 通常スコア計算
        severe_score = int(selected_option['severe_score'])
        if commonscore == 0 and severe_score == 1:
            commonscore += severe_score
            display_output(f"共通スコアが{severe_score}に更新されました。")
        elif severe_score == 0:
            display_output(f"現在のスコアは{commonscore}です。スコアは変わりません。")
        elif commonscore == 1:
            display_output(f"現在のスコアはすでに{commonscore}です。スコアは変わりません。")
        display_output(f"現在の共通質問によるスコア: {commonscore}")

    display_output(f"\n最終的な共通スコア: {commonscore}")
    return commonscore, special_urgency
