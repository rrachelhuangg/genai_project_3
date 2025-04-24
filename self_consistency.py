from google import genai
import json
import os

client = genai.Client(api_key="AIzaSyDDK-2nQscZir1LCJ6R-CTDgBg2NIs0Qw0")
output_file = "output.txt"

def call_gemini(prompt, code):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"Prompt: {prompt}:Code: {code}"
    )
    return response.text

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
                    file.write(call_gemini(prompt, snippet))