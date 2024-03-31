import random
import wikipedia

# Define responses for the chatbot
responses = {
    "hello": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm good, thank you!", "I'm doing well, thanks for asking.", "All good!"],
    "bye": ["Goodbye!", "See you later!", "Bye!"],
    "default": ["I'm not sure what you mean...", "Could you please rephrase that?", "I didn't get that."]
}

# Define a dictionary to store user information
user_info = {}

# Greeting and farewell messages
GREETING = "Welcome to the Chatbot! Type 'bye' to exit."
FAREWELL = "Goodbye! Have a great day!"

# Function to generate response
def generate_response(user_input, user_name=None, context=None):
    user_input = user_input.lower()
    if user_input == "what's my name?":
        if user_name:
            return f"Your name is {user_name}."
        else:
            return "I'm sorry, I don't remember your name. Please tell me your name."
    elif user_input.startswith("my name is "):
        user_name = user_input.split("is ")[-1]
        user_info['name'] = user_name
        return f"Nice to meet you, {user_name}!"
    elif user_input.startswith("tell me about"):
        topic = user_input.split("tell me about ")[-1]
        user_info['topic'] = topic
        try:
            # Use Wikipedia API to search for the topic
            wikipedia.set_lang("en")  # Set language to English
            page = wikipedia.page(topic)
            url = page.url  # Get Wikipedia page URL
            return f"Sure, I can tell you about {topic}. You can read more about it here: {url}"
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple options, provide suggestions
            return f"I found multiple options for '{topic}'. Please be more specific."
        except wikipedia.exceptions.PageError:
            # If page does not exist, notify the user
            return f"I'm sorry, I couldn't find information about '{topic}' on Wikipedia."
    elif user_input.startswith("i like "):
        user_info['topic'] = user_input.split("i like ")[-1]
        return f"That's interesting! I can tell you more about {user_info['topic']}."
    elif user_info.get('topic') and user_input.startswith(user_info['topic']):
        # Respond to the user's previous message if the topic exists
        return f"I see you like {user_info['topic']}. Did you know that..."
    elif user_input in responses:
        return random.choice(responses[user_input])
    else:
        return random.choice(responses["default"])
recommendations = {
    "movies": ["The Shawshank Redemption", "The Godfather", "Pulp Fiction"],
    "books": ["To Kill a Mockingbird", "The Great Gatsby", "Pride and Prejudice"],
    "music": ["The Beatles", "Queen", "The Rolling Stones"]
}

# Function to generate recommendation
def generate_recommendation():
    category = random.choice(list(recommendations.keys()))
    item = random.choice(recommendations[category])
    return f"I recommend checking out {item} in the {category} category."
# Main loop to interact with the user
def main():
    print(GREETING)
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'bye':
            print(generate_response(user_input))
            print(FAREWELL)
            break
        else:
            user_name = user_info.get('name')
            if user_input.startswith("recommend me"):
                if user_info.get('topic'):
                    print("Bot:", generate_recommendation())
                else:
                    print("Bot:", "Please tell me what you like first.")
            elif user_input.startswith("i like "):
                user_info['topic'] = user_input.split("i like ")[-1]
                print("Bot:", generate_response(user_input, user_name, user_info))
                print("Bot:", generate_recommendation())
            else:
                print("Bot:", generate_response(user_input, user_name, user_info))

if __name__ == "__main__":
    main()