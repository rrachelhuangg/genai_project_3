from google import genai
import json
import os

client = genai.Client(api_key="AIzaSyDDK-2nQscZir1LCJ6R-CTDgBg2NIs0Qw0")
output_file = "output.txt"

def call_gemini(prompt, code):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}:{code}"
    )
    return response.text

files = [f for f in os.listdir("tasks_code") if os.path.isfile(os.path.join("tasks_code", f))]
files.sort()
for key in range(11, 16):
    with open (f"tasks_code/{files[key-1]}", "r") as file:
        print("FILE: ", file)
        snippet = file.read()
    with open(output_file, "a") as file:
        file.write(f"PROBLEM {key}\n")
        file.write(call_gemini("Please generate 3 similar problems to this provided code snippet and solve them", snippet))
        key += 1
