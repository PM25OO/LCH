from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("Deepseek_API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
messages = [{"role": "system", "content": "你是一个乐于助人的助手，用中文回答问题。"}]

while True:
    user_input = input("你: ")
    if user_input.lower() in ["exit()", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-reasoner", messages=messages, stream=True
    )

    reasoning_content = ""
    content = ""
    should_print1, should_print2 = True, True

    print(f"\n思考中...\n")
    for chunk in response:

        if chunk.choices[0].delta.reasoning_content:
            print(chunk.choices[0].delta.reasoning_content, end="")
            reasoning_content += chunk.choices[0].delta.reasoning_content
        if chunk.choices[0].delta.content:
            if should_print2:
                print(f"\n\nDeepSeek: ")
                should_print2 = False
            print(chunk.choices[0].delta.content, end="")
            content += chunk.choices[0].delta.content

    print(f"\n")

    messages.append({"role": "assistant", "content": content})
