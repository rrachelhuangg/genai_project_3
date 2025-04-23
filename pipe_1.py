from google import genai
import json
import os
import ollama

ollama_model = "llava:7b-v1.6"

subset_1_output_dir = "subset_1"
client = genai.Client(api_key="AIzaSyDDK-2nQscZir1LCJ6R-CTDgBg2NIs0Qw0")

def call_gemini(prompt, code):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}:{code}"
    )
    return response.text

def call_ollama(prompt, code):
    response = ollama.chat(
        model=ollama_model,
        messages = [
            {
                "role":"user",
                "content":f"{prompt}:{code}",
            }
        ]
    )
    return response["message"]["content"]

def run_pipe():
    zero_shot_prompts = {}
    with open("zero_shot_prompts.json", "r") as file:
        zero_shot_prompts = json.load(file)
    few_shot_examples = [f for f in os.listdir("few_shot_examples") if os.path.isfile(os.path.join("few_shot_examples", f))]
    files = [f for f in os.listdir("tasks_code") if os.path.isfile(os.path.join("tasks_code", f))]
    for key in range(1,6):
        #zero shot
        prompt = zero_shot_prompts[str(key)]
        snippet = ""
        for f in files:
            if int(f[f.find("k")+1:f.find(".")]) == key:
                #zero shot
                print("FILE: ", f"tasks_code/{f}")
                with open(f"tasks_code/{f}", "r") as file:
                    snippet = file.read()
                response = call_gemini(prompt, snippet)
                with open(f"{subset_1_output_dir}/gemini_task{key}_zero_shot.txt", "w") as file:
                    file.write(response)
                response = call_ollama(prompt, snippet)
                with open(f"{subset_1_output_dir}/ollama_task{key}_zero_shot.txt", "w") as file:
                    file.write(response)
                #few shot
                for f in few_shot_examples:
                    if int(f[:f.find(".")]) == key:
                        with open(f"few_shot_examples/{f}", "r") as file:
                            few_shot = file.read()
                            response = call_gemini(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_1_output_dir}/gemini_task{key}_few_shot.txt", "w") as file:
                                file.write(response)
                            response = call_ollama(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_1_output_dir}/ollama_task{key}_few_shot.txt", "w") as file:
                                file.write(response)

if __name__ == '__main__':
    run_pipe()
