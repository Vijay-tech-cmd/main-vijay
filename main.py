from dotenv import load_dotenv
import os
import anthropic
from halo import Halo
import pprint

load_dotenv() 
pp = pprint.PrettyPrinter(indent=5)

def generate_function(user_message):
    spinner = Halo(text='Loading...',spinner='circle')
    spinner.start()

    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))
    response = client.messages.create(
        model = os.getenv("MODEL_NAME"),
        max_tokens = 500,
        temperature = 1,
        system = "Response in short and clear sentence.",
        messages = [
            {
                "role" : "user",
                "content" : user_message
            }
        ]
    )
    spinner.stop()

    print("Reguest: ")
    pp.pprint(user_message)
    print("Response: ")
    pp.pprint(response.content)

    return response.content

def main():
    while True:
        input_text = input("You: ")

        if input_text.lower() == "quit":
            break
        response = generate_function(input_text)
        print(f"Claude: {response}")

if __name__ == "__main__":
    main()