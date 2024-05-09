import json
import random

# Load responses from JSON file
with open('responses.json') as file:
    responses = json.load(file)

# Function to generate a response based on user input
def generate_response(user_input):
    if 'hello' in user_input.lower() or 'hi' in user_input.lower():
        return random.choice(responses['greetings']), False
    elif 'bye' in user_input.lower() or 'goodbye' in user_input.lower():
        return random.choice(responses['farewell']), True
    elif '?' in user_input:
        return random.choice(responses['questions']), False
    elif 'yes' in user_input.lower() or 'sure' in user_input.lower() or 'yeah' in user_input.lower():
        return random.choice(responses['affirmative']), False
    elif 'no' in user_input.lower() or 'nah' in user_input.lower():
        return random.choice(responses['negative']), False
    else:
        return random.choice(responses['generic']), False

# Main function for chatting
def chat():
    name = input("Enter your name: ")
    print(f"Hello, {name}! I'm your chatbot. How can I assist you today?")
    while True:
        user_input = input(f"{name}: ")
        response, exit_chat = generate_response(user_input)
        print("Chatbot:", response)
        if exit_chat:
            print("...")
            break

# Start the conversation
chat()
