from module_g_gui import run_gui_app
from module_a_symptom_input import process_symptom, find_most_similar_word
from module_b_category_questions import ask_category_questions, find_level2_category
from module_c_common_questions import ask_common_questions
from module_d_urgency import find_urgency_by_score

def main(display_output, ask_user):
    # 1. 症状入力
    user_input = ask_user("症状について説明してください: ")
    embedding = process_symptom(user_input, display_output)
    if embedding is None:
        display_output("Embeddingの取得に失敗しました。")
        return
    
    # 2. 類似症状検索
    similar_word = find_most_similar_word(embedding)
    display_output(f"似ている症状: {similar_word}")
    
    # 3. カテゴリ検索
    categories = find_level2_category(similar_word, display_output)
    if not categories:
        display_output("カテゴリが見つかりませんでした。")
        return
    
    # 4. カテゴリ質問
    current_score = 0
    current_score = ask_category_questions(categories, current_score, similar_word, display_output, ask_user)
    
    # 5. 共通質問
    commonscore, special_urgency = ask_common_questions(display_output, ask_user)
    
    # 6. 総合スコア計算
    final_score = current_score + commonscore
    display_output(f"重症度スコア: {final_score}")
    
    # 7. 緊急性判定
    find_urgency_by_score(final_score, display_output, special_urgency)

if __name__ == "__main__":
    run_gui_app(main)
