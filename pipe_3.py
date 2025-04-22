from google import genai
import json
import os
import ollama

ollama_model = "llava:7b-v1.6"

subset_3_output_dir = "subset_3"

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
    few_shot_examples.sort()
    files = [f for f in os.listdir("tasks_code") if os.path.isfile(os.path.join("tasks_code", f))]
    for key in range(6, 11):
        #few shot
        prompt = zero_shot_prompts[str(key)]
        print("PROMPT FEW SHOT: ", prompt)
        snippet = ""
        with open (f"tasks_code/{files[int(key)-1]}", "r") as file:
            snippet = file.read()
        with open(f"few_shot_examples/{few_shot_examples[key-1]}", "r") as file:
            few_shot = file.read()
            response = call_gemini(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
            with open(f"{subset_3_output_dir}/gemini_task{key}_few_shot.txt", "w") as file:
                file.write(response)
            response = call_ollama(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
            with open(f"{subset_3_output_dir}/ollama_task{key}_few_shot.txt", "w") as file:
                file.write(response)
        #chain of thought
        print("PROMPT CHAIN OF THOUGHT: ", prompt)
        response = call_gemini(prompt + "\t" + "Do it step by step: ", snippet)
        with open(f"{subset_3_output_dir}/gemini_task{key}_chain_of_thought.txt", "w") as file:
            file.write(response)
        response = call_ollama(prompt + "\t" + "Do it step by step: ", snippet)
        with open(f"{subset_3_output_dir}/ollama_task{key}_chain_of_thought.txt", "w") as file:
            file.write(response)

if __name__ == '__main__':
    run_pipe()
