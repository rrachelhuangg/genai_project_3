import os
import json
from mistralai import Mistral

model = "mistral-large-latest"
api_key = ""
client = Mistral(api_key=api_key)

def call_mistral(prompt, code):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"Prompt: {prompt}, Code: {code}",
            },
        ]
    )
    return chat_response.choices[0].message.content

output_file = "output.txt"

files = [f for f in os.listdir("tasks_code") if os.path.isfile(os.path.join("tasks_code", f))]
zero_shot_prompts = {}
with open("zero_shot_prompts.json", "r") as file:
    zero_shot_prompts = json.load(file)
for key in range(22, 23):
    prompt = zero_shot_prompts[str(key)]
    snippet = ""
    for f in files:
        if int(f[f.find("k")+1:f.find(".")]) == key:
            #zero shot
            print("FILE: ", f"tasks_code/{f}")
            with open(f"tasks_code/{f}", "r") as file:
                snippet = file.read()
            with open(output_file, "a") as file:
                file.write(f"PROBLEM {key} \n")
                for i in range(5):
                    file.write(call_mistral(prompt, snippet))
