from module_f_neo4j import graph

def find_urgency_by_score(total_score, display_output, special_urgency=None):
    if special_urgency:
        display_output(f"\n特別ルールに基づき緊急性を適用: {special_urgency}")
        return

    query = """
    MATCH (u:Urgency)
    WHERE u.severe_score = $total_score
    RETURN u.Name AS urgency_name
    """
    try:
        result = graph.run(query, total_score=total_score).data()
    except Exception as e:
        display_output(f"緊急性判定中にDBエラー: {e}")
        return

    display_output(f"\n最終的なスコア: {total_score}")
    if result:
        urgency_name = result[0]['urgency_name']
        display_output(f"最終スコアに一致するUrgencyノードの名前: {urgency_name}")
    else:
        display_output("一致するUrgencyノードが見つかりませんでした。")
