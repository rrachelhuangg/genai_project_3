import os
from mistralai import Mistral

api_key = "CM9L45tyGDIXU04Y3Ewjha2JNILCd1As"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

content = ""
with open("temp.txt", "r") as file:
    content = file.read()

def call_mistral(content):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"{content}",
            },
        ]
    )
    return chat_response.choices[0].message.content

with open("output.txt", "w") as file:
    file.write(f"PROBLEM {18} \n")
    file.write(call_mistral(content))