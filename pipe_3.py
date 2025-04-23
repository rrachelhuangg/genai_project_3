from google import genai
import json
import os
import ollama
import openai

ollama_model = "llava:7b-v1.6"

subset_3_output_dir = "subset_3"
client = genai.Client(api_key="AIzaSyDDK-2nQscZir1LCJ6R-CTDgBg2NIs0Qw0")
openai.api_key = "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"

def call_gpt4o(prompt, code):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}:{code}"}
        ]
    )
    return response.choices[0].message.content

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
    for key in range(11, 16):
        prompt = zero_shot_prompts[str(key)]
        snippet = ""
        for f in files:
            if int(f[f.find("k")+1:f.find(".")]) == key:
                #few shot
                print("FILE: ", f"tasks_code/{f}")
                with open(f"tasks_code/{f}", "r") as file:
                    snippet = file.read()
                for f in few_shot_examples:
                    if int(f[:f.find(".")]) == key:
                        with open(f"few_shot_examples/{f}", "r") as file:
                            few_shot = file.read()
                            response = call_ollama(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_3_output_dir}/ollama_task{key}_few_shot.txt", "w") as file:
                                file.write(response)
                            response = call_gpt4o(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_3_output_dir}/gpt4o_task{key}_few_shot.txt", "w") as file:
                                file.write(response)
                #chain of thought
                print("PROMPT CHAIN OF THOUGHT: ", prompt)
                response = call_ollama(prompt + "\t" + "Do it step by step: ", snippet)
                with open(f"{subset_3_output_dir}/ollama_task{key}_chain_of_thought.txt", "w") as file:
                    file.write(response)
                response = call_gpt4o(prompt + "\t" + "Do it step by step: ", snippet)
                with open(f"{subset_3_output_dir}/gpt4o_task{key}_chain_of_thought.txt", "w") as file:
                    file.write(response)

if __name__ == '__main__':
    run_pipe()
