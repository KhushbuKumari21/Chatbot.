import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Menu
import wikipedia
import os
import warnings
import spacy
from chatbot import Chat, register_call
import datetime
import webbrowser
import random
import speech_recognition as sr
import pyaudio


warnings.filterwarnings("ignore")

@register_call("whoIs")
def who_is(session, query):
    try:
        return wikipedia.summary(query)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  
        return f"Did you mean: {' | '.join(options)}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find information about that."

@register_call("currentDateTime")
def current_date_time(session, query):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@register_call("openWebsite")
def open_website(session, query):
    try:
        url = query.split()[-1]
        webbrowser.open(url)
        return f"Opening {url}..."
    except Exception as e:
        return f"Failed to open {url}: {str(e)}"

@register_call("joke")
def tell_joke(session, query):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Parallel lines have so much in common. It’s a shame they’ll never meet. 📐",
        "I told my wife she should embrace her mistakes. She gave me a hug. 🤗",
        "I'm reading a book on anti-gravity. It's impossible to put down! 📚",
        "I told my computer I needed a break and now it won't stop showing me pictures of Kit Kats. 🍫"
    ]
    return random.choice(jokes)

class Chatbot:
    def __init__(self, name):
        self.name = name
        self.chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "C:\\Users\\hp\\Documents\\chatbotnew\\Chatbot-In-Python-master\\examples\\Example.template"))
        self.nlp = spacy.load("en_core_web_sm")
        self.chat_history = []

    def generate_response(self, user_input):
        doc = self.nlp(user_input)

        if "hey" in user_input.lower():
            return "Hey! What is your good name? 😊"
        elif "my name is" in user_input.lower():
            name_start = user_input.lower().index("my name is") + len("my name is")
            user_name = user_input[name_start:].strip()
            return f"Nice to meet you {user_name}, welcome! 👋"
        elif "what is python" in user_input.lower():
            return "Python is a high-level programming language known for its simplicity and readability. 🐍"
        elif "what is java" in user_input.lower():
            return "Java is an object-oriented programming language known for its simplicity, portability, and security. ☕️"
        elif "can you give name of other programming language" in user_input.lower():
            return "Sure, there are many programming languages like Java, C++, PHP, JavaScript, and more. 🖥️"
        elif "thank" in user_input.lower():
            return "You're welcome! 😊"
        elif "bye" in user_input.lower():
            return "Goodbye! Have a great day. 👋"

        elif any(token.text.lower() == "python" for token in doc):
            return "I see you're interested in Python programming. What specific information would you like to know? 🐍"

        else:
            response = self.chat.respond(user_input)
            if not response:
                try:
                    response = who_is(None, user_input)
                except Exception:
                    response = "Sorry, I couldn't find information about that. 😞"
            self.chat_history.append(f"You: {user_input}\nSbot: {response}\n")
            return response

    def save_chat_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.writelines(self.chat_history)
            messagebox.showinfo("Save Successful", "Chat history saved successfully.")
        else:
            messagebox.showwarning("Save Cancelled", "Save operation cancelled.")

    def clear_chat_history(self):
        self.chat_history = []

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot Development App")

        self.chat_history = scrolledtext.ScrolledText(master, width=60, height=20, font=("Helvetica", 12))
        self.chat_history.pack(padx=10, pady=10)

        self.user_input = tk.Entry(master, width=60, font=("Helvetica", 12))
        self.user_input.pack(padx=10, pady=(0, 10))

        self.submit_button = tk.Button(master, text="Send", command=self.submit, font=("Helvetica", 12))
        self.submit_button.pack(padx=10, pady=(0, 10))

        self.save_button = tk.Button(master, text="Save Chat", command=self.save_chat, font=("Helvetica", 12))
        self.save_button.pack(padx=10, pady=(0, 10))

        self.clear_button = tk.Button(master, text="Clear Chat", command=self.clear_chat, font=("Helvetica", 12))
        self.clear_button.pack(padx=10, pady=(0, 10))

        self.speech_button = tk.Button(master, text="Speech Input", command=self.speech_input, font=("Helvetica", 12))
        self.speech_button.pack(padx=10, pady=(0, 10))

        self.chatbot = Chatbot("Sbot")

        self.help_button = tk.Button(master, text="Help", command=self.show_help, font=("Helvetica", 12))
        self.help_button.pack(padx=10, pady=(0, 10))

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def submit(self):
        user_text = self.user_input.get()
        self.user_input.delete(0, tk.END)

        response = self.chatbot.generate_response(user_text)
        self.update_chat_history(f"You: {user_text}\nSbot: {response}")

        if "bye" in user_text.lower():
            self.master.destroy()

    def save_chat(self):
        self.chatbot.save_chat_history()

    def clear_chat(self):
        self.chat_history.configure(state='normal')
        self.chat_history.delete('1.0', tk.END)
        self.chat_history.configure(state='disabled')

    def speech_input(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            user_input = self.recognizer.recognize_google(audio)
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, user_input)
            self.submit()
        except sr.UnknownValueError:
            messagebox.showwarning("Speech Recognition", "Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            messagebox.showerror("Speech Recognition", "Speech recognition service is unavailable.")

    def update_chat_history(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + '\n\n')
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

    def show_help(self):
        help_text = """Welcome to the Chatbot Development App!
        
        This chatbot can:
        - Provide information about Python and Java.
        - Answer general questions and engage in small talk.
        - Retrieve information from Wikipedia.
        - Tell jokes for a good laugh.
        - Show the current date and time.
        - Open websites in your default browser.
        - Save chat history to a text file.
        - Clear the chat history.
        - Accept speech input for queries.
        
        Feel free to ask questions or just say hi!
        """
        messagebox.showinfo("Chatbot Help", help_text)

def main():
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    
  
    menubar = Menu(root)
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save Chat", command=chatbot_gui.save_chat)
    file_menu.add_command(label="Clear Chat", command=chatbot_gui.clear_chat)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    
   
    root.config(menu=menubar)
    
    root.mainloop()

if __name__ == "__main__":
    main()
