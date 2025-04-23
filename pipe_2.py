from google import genai
import json
import os
import openai

ollama_model = "llava:7b-v1.6"

subset_2_output_dir = "subset_2"
client = genai.Client(api_key="AIzaSyDDK-2nQscZir1LCJ6R-CTDgBg2NIs0Qw0")
openai.api_key = "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"

def call_gemini(prompt, code):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}:{code}"
    )
    return response.text

def call_gpt4o(prompt, code):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}:{code}"}
        ]
    )
    return response.choices[0].message.content

def run_pipe():
    zero_shot_prompts = {}
    with open("zero_shot_prompts.json", "r") as file:
        zero_shot_prompts = json.load(file)
    few_shot_examples = [f for f in os.listdir("few_shot_examples") if os.path.isfile(os.path.join("few_shot_examples", f))]
    files = [f for f in os.listdir("tasks_code") if os.path.isfile(os.path.join("tasks_code", f))]
    for key in range(6, 11):
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
                with open(f"{subset_2_output_dir}/gemini_task{key}_zero_shot.txt", "w") as file:
                    file.write(response)
                response = call_gpt4o(prompt, snippet)
                with open(f"{subset_2_output_dir}/gpt4o_task{key}_zero_shot.txt", "w") as file:
                    file.write(response)
                #few shot
                for f in few_shot_examples:
                    if int(f[:f.find(".")]) == key:
                        with open(f"few_shot_examples/{f}", "r") as file:
                            few_shot = file.read()
                            response = call_gemini(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_2_output_dir}/gemini_task{key}_few_shot.txt", "w") as file:
                                file.write(response)
                            response = call_gpt4o(prompt + "\t" + "Here are some examples: " + few_shot, snippet)
                            with open(f"{subset_2_output_dir}/gpt4o_task{key}_few_shot.txt", "w") as file:
                                file.write(response)

if __name__ == '__main__':
    run_pipe()
