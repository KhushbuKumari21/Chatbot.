import tkinter as tk
from tkinter import scrolledtext
import wikipedia
from chatbot import Chat, register_call
import os
import warnings
import spacy

warnings.filterwarnings("ignore")

class Chatbot:
    def __init__(self, name):
        self.name = name
        self.chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), r"C:\Users\hp\Documents\chatbotnew\Chatbot-In-Python-master\examples\Example.template"))


        self.nlp = spacy.load("en_core_web_sm")

    def generate_response(self, user_input):
        doc = self.nlp(user_input)
        if "hey" in user_input.lower():
            return "Hey! What is your good name?"
        elif "my name is" in user_input.lower():
            name_start = user_input.lower().index("my name is") + len("my name is")
            user_name = user_input[name_start:].strip()
            return f"Nice to meet you {user_name}, welcome!"
        elif "what is python" in user_input.lower():
            return "Python is a high-level programming language known for its simplicity and readability."
        elif "what is java" in user_input.lower():
            return "Java is an object-oriented programming language known for its simplicity, portability, and security."
        elif "can you give name of other programming language" in user_input.lower():
            return "Sure, there are many programming languages like Java, C++, PHP, JavaScript, and more."
        elif "thank" in user_input.lower():
            return "You're welcome!"
        elif any(token.text.lower() == "python" for token in doc):
            return "I see you're interested in Python programming. What specific information would you like to know?"
        else:
            response = self.chat.respond(user_input)
            if not response:
                response = self.handle_wikipedia(user_input)
            return response

    def handle_wikipedia(self, user_input):
        try:
            summary = wikipedia.summary(user_input)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:3]  # Limit options to 3 for simplicity
            return f"Did you mean: {' | '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find information about that."

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")

        self.chat_history = scrolledtext.ScrolledText(master, width=60, height=20, font=("Helvetica", 12))
        self.chat_history.pack(padx=10, pady=10)

        self.user_input = tk.Entry(master, width=60, font=("Helvetica", 12))
        self.user_input.pack(padx=10, pady=(0, 10))

        self.submit_button = tk.Button(master, text="Send", command=self.submit, font=("Helvetica", 12))
        self.submit_button.pack(padx=10, pady=(0, 10))

        self.chatbot = Chatbot("Sbot")

    def submit(self):
        user_text = self.user_input.get()
        self.user_input.delete(0, tk.END)

        response = self.chatbot.generate_response(user_text)
        self.update_chat_history(f"You: {user_text}\nSbot: {response}")

        if "bye" in user_text.lower():
            self.master.destroy()

    def update_chat_history(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + '\n\n')
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

def main():
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
