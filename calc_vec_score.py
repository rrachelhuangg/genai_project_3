import pandas as pd
import openai
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import AutoModel, AutoTokenizer
import torch.nn.functional as F

df = pd.read_excel('Results_Report.xlsx')
openai.api_key = ""

def call_gpt4o(code1, code2):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a code analyst."},
            {"role": "user", "content": f"Analyze the accuracy and similarities/differences of these two snippets in two concise sentences. Don't include redundant or contradictory information. {code1} and {code2}"}
        ]
    )
    return response.choices[0].message.content

i = 0
model_1_results = []
model_2_results = []

for col in df.columns:
    if 'Model1' in col and i == 1:
        for entry in df[col]:
            model_1_results += [entry]
        i = 0
    elif 'Model1' in col and i == 0:
        i += 1
    elif 'Model2' in col and i == 1:
        for entry in df[col]:
            model_2_results += [entry]
        i = 0
    elif 'Model2' in col and i == 0:
        i += 1

model_1_results = model_1_results[56:]
model_2_results = model_2_results[56:]
length = len(model_1_results)

checkpoint = "Salesforce/codet5p-110m-embedding"
device = "cpu"
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True).to(device)

def get_embedding(text):
    if not text or not isinstance(text, str) or text.strip() == "":
        return torch.zeros(model.config.hidden_size)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        last_hidden_state = model(**inputs)[0]
    
    if last_hidden_state.ndim == 3:
        embedding = last_hidden_state.mean(dim=1)
    else:
        embedding = last_hidden_state
    
    return embedding.squeeze()

model_1_embeddings = torch.stack([get_embedding(text) for text in model_1_results])
model_2_embeddings = torch.stack([get_embedding(text) for text in model_2_results])

cosine_scores = F.cosine_similarity(model_1_embeddings, model_2_embeddings)
scores_list = cosine_scores.tolist()
for i, score in enumerate(scores_list):
    print(f"Entries {i} with similarity score of {score:.6f}")
