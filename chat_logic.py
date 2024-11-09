import wikipedia
import random
from datetime import datetime

registered_calls = {}

def register_call(func_name):
    """Decorator to register a function as a callable query."""
    def wrapper(func):
        registered_calls[func_name] = func
        return func
    return wrapper

class Chat:
    """Chatbot logic to respond to user inputs."""
    def __init__(self, template_path):
        self.template_path = template_path
        self.user_name = None  # Store the user's name
        self.chat_history = []  # Store conversation history

    def respond(self, user_input):
        """Generate a response based on user input."""
        user_input = user_input.lower()
        self.chat_history.append(f"User: {user_input}")  # Log user input

        # Handle greetings
        if "hello" in user_input or "hi" in user_input or "hey" in user_input:
            response = self.greet_user()
        elif "my name is" in user_input:
            response = self.set_user_name(user_input)
        elif "thank" in user_input:
            response = self.thank_user()
        elif "can you give a favor" in user_input or "can you help me" in user_input:
            response = "What type of favor would you like?"
        elif "delete chat" in user_input:
            response = self.delete_chat()
        elif "save chat" in user_input:
            response = self.save_chat()
        elif "what is python" in user_input:
            response = "Python is a high-level, interpreted programming language known for its ease of use and readability."
        else:
            response = self.default_response(user_input)
            for func_name, func in registered_calls.items():
                if func_name in user_input:
                    response = func(None, user_input)  # Call the registered function

        self.chat_history.append(f"Chatbot: {response}")  # Log chatbot response
        return response

    def greet_user(self):
        """Greet the user by name if available."""
        if self.user_name:
            return f"Hello, {self.user_name}! How can I assist you today?"
        return "Hello! What's your name?"

    def set_user_name(self, user_input):
        """Set the user's name based on their input."""
        name = user_input.replace("my name is ", "").strip()
        self.user_name = name
        return f"Nice to meet you, {name}!"

    def thank_user(self):
        """Respond to a thank you."""
        return "You're welcome! If you have more questions, feel free to ask."

    def delete_chat(self):
        """Delete the chat history."""
        self.chat_history = []  # Clear the chat history
        return "Chat history deleted successfully."

    def save_chat(self):
        """Save the chat history to a file."""
        with open("chat_history.txt", "w") as file:
            for line in self.chat_history:
                file.write(line + "\n")
        return "Chat history saved successfully."

    def default_response(self, user_input):
        """Provide a default response if the input doesn't match known patterns."""
        responses = [
            "I'm not sure how to respond to that. Can you ask something else?",
            "Let's talk about something else. How can I assist you?",
            "Could you clarify that for me? Perhaps you can ask something different.",
        ]
        return random.choice(responses)

# Registering a call for Wikipedia queries
@register_call("who is")
def who_is(session, query):
    """Fetch a summary from Wikipedia based on the user's query."""
    try:
        topic = query.replace("who is ", "").strip()
        return wikipedia.summary(topic, sentences=1)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  # Suggesting up to 3 options
        return f"Did you mean: {' | '.join(options)}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find information about that."

# Registering a call to tell a joke
@register_call("tell me a joke")
def tell_joke(session, query):
    """Return a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Parallel lines have so much in common. It’s a shame they’ll never meet. 📐",
        "I told my wife she should embrace her mistakes. She gave me a hug. 🤗",
        "I'm reading a book on anti-gravity. It's impossible to put down! 📚",
        "I told my computer I needed a break and now it won't stop showing me pictures of Kit Kats. 🍫"
    ]
    return random.choice(jokes)

# Registering a call for current date and time
@register_call("current date")
def current_date(session, query):
    """Return the current date and time."""
    return f"The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
