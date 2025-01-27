import os
import openai

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("APIキーが設定されていません。")

def get_text_embedding(text):
    try:
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return  response.data[0].embedding
    except Exception as e:
        print(f"Error getting text embedding: {e}")
        def main():
            text = "OpenAIの埋め込みを取得します。"
            embedding = get_text_embedding(text)
            if embedding:
                print("埋め込み取得成功:", embedding)
            else:
                print("埋め込み取得失敗")
        
        if __name__ == "__main__":
            API_KEY = os.getenv("OPENAI_API_KEY")
            if not API_KEY:
                raise ValueError("APIキーが設定されていません。")

            openai.api_key = API_KEY

            def get_text_embedding(text):
                try:
                    response = openai.embeddings.create(
                        input=text,
                        model="text-embedding-ada-002"
                    )
                    return response.data[0].embedding
                except Exception as e:
                    print(f"Error getting text embedding: {e}")
                    return None

            def main():
                text = "OpenAIの埋め込みを取得します。"
                embedding = get_text_embedding(text)
                if embedding:
                    print("埋め込み取得成功:", embedding)
                else:
                    print("埋め込み取得失敗")

            if __name__ == "__main__":
                main()
