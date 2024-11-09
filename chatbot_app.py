import tkinter as tk
from chat_logic import Chat
import speech_recognition as sr

class ChatbotGUI:
    """GUI for the chatbot application."""
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        master.geometry("600x500")
        
        # Chat area setup
        self.chat_frame = tk.Frame(master)
        self.chat_frame.pack(pady=10)

        self.text_area = tk.Text(self.chat_frame, height=15, width=70, bg="#f0f0f0", font=("Arial", 12))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # User input area
        self.entry = tk.Entry(master, width=60, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.submit)

        # Buttons setup
        self.submit_button = tk.Button(master, text="Send", command=self.submit, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.submit_button.pack(pady=5)

        self.save_button = tk.Button(master, text="Save Chat", command=self.save_chat, bg="#008CBA", fg="white", font=("Arial", 12))
        self.save_button.pack(pady=5)

        self.clear_button = tk.Button(master, text="Clear Chat", command=self.clear_chat, bg="#f44336", fg="white", font=("Arial", 12))
        self.clear_button.pack(pady=5)

        self.voice_button = tk.Button(master, text="Speak", command=self.voice_input, bg="#FF9800", fg="white", font=("Arial", 12))
        self.voice_button.pack(pady=5)

        # Initialize chatbot
        self.chatbot = Chat("D:\\chatbot\\Example.template")
        self.text_area.insert(tk.END, "Welcome to Chatbot!\n")

    def submit(self, event=None):
        """Submit user input and get chatbot response."""
        user_input = self.entry.get()
        self.text_area.insert(tk.END, f"You: {user_input}\n", "user")
        response = self.chatbot.respond(user_input)
        self.text_area.insert(tk.END, f"Chatbot: {response}\n", "bot")
        self.entry.delete(0, tk.END)
        self.text_area.see(tk.END)

    def save_chat(self):
        """Save the current chat history."""
        response = self.chatbot.save_chat()
        self.text_area.insert(tk.END, f"Chatbot: {response}\n", "bot")
        self.text_area.see(tk.END)

    def clear_chat(self):
        """Clear the chat history."""
        self.text_area.delete(1.0, tk.END)
        response = self.chatbot.delete_chat()
        self.text_area.insert(tk.END, f"Chatbot: {response}\n", "bot")
        self.text_area.see(tk.END)

    def voice_input(self):
        """Capture voice input from the user."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_area.insert(tk.END, "Listening...\n", "bot")
            audio = recognizer.listen(source)

            try:
                user_input = recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, f"You: {user_input}\n", "user")
                response = self.chatbot.respond(user_input)
                self.text_area.insert(tk.END, f"Chatbot: {response}\n", "bot")
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Chatbot: Sorry, I did not understand that.\n", "bot")
            except sr.RequestError as e:
                self.text_area.insert(tk.END, f"Chatbot: Could not request results; {e}\n", "bot")
            except Exception as e:
                self.text_area.insert(tk.END, f"Chatbot: An error occurred: {str(e)}\n", "bot")
            
            self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatbotGUI(root)
    root.mainloop()
