import tkinter as tk
from tkinter import scrolledtext
import threading
import queue

def run_gui_app(main_logic_function):
    class ChatUI:
        def __init__(self, root, main_logic_function):
            self.root = root
            self.root.title("チャット形式の問診システム")

            # チャットログ表示用（スクロール可能テキスト）
            self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled')
            self.chat_display.pack(padx=10, pady=10)

            # 入力欄と送信ボタン
            self.entry_frame = tk.Frame(root)
            self.entry_frame.pack(padx=10, pady=(0,10), fill='x')

            self.user_input_entry = tk.Entry(self.entry_frame)
            self.user_input_entry.pack(side=tk.LEFT, fill='x', expand=True)

            self.send_button = tk.Button(self.entry_frame, text="送信", command=self.on_send)
            self.send_button.pack(side=tk.LEFT, padx=5)

            # ユーザの入力を受け取るためのキュー
            self.input_queue = queue.Queue()

            # メインロジックを別スレッドで実行
            self.thread = threading.Thread(target=main_logic_function, args=(self.display_message, self.get_user_input), daemon=True)
            self.thread.start()

        def on_send(self):
            text = self.user_input_entry.get().strip()
            if not text:
                self.append_message("システム:空文字なので送信しません。")
                return
            self.append_message("あなた: " + text)
            self.input_queue.put(text)
            self.user_input_entry.delete(0, tk.END)

        def append_message(self, message: str):
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, message + "\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state='disabled')

        def display_message(self, message: str):
            self.append_message("システム: " + message)

        def get_user_input(self, prompt: str = "") -> str:
            if prompt:
                self.append_message("システム: " + prompt)
            return self.input_queue.get()

    root = tk.Tk()
    app = ChatUI(root, main_logic_function)
    root.mainloop()
