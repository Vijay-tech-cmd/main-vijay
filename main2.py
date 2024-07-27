from dotenv import load_dotenv
import os
import anthropic
from halo import Halo
import pprint
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

load_dotenv()

pp=pprint.PrettyPrinter(indent=4)

memory = ConversationBufferMemory(return_messages=True)

def generate_response(user_message):
    spinner = Halo(text='Loading...',spinner='dots')
    spinner.start()

    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))

    conversation_history = memory.chat_memory.messages
    messages = []
    
    for message in conversation_history:
        if isinstance(messages, HumanMessage):
            messages.append({"role" : "user", "content" : message.content})
        elif isinstance(messages, AIMessage):
            messages.append({"role" : "assistant", "content" : message.content})
    messages.append({
        "role" : "user",
        "content" : user_message
    })        

    response = client.messages.create(
        model = os.getenv("MODEL_NAME"),
        max_tokens = 500,
        temperature = 0,
        messages = messages
    )
    spinner.stop()

    print("Reguest: ")
    pp.pprint(user_message)
    print("Response: ")
    pp.pprint(response.content)

    memory.chat_memory.add_user_message(user_message)
    memory.chat_memory.add_ai_message(response.content)

    return response.content   

def main():
    while True:
        input_text = input("You: ")

        if input_text.lower() == "quit":
            break
        response = generate_response(input_text)
        print(f"Claude: {response}")

if __name__ == "__main__":
    main()         