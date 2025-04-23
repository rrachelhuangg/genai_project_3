import pandas as pd

df = pd.read_excel('GenAI_Project_3_Results.xlsx')

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

model_1_results = model_1_results[:30]
model_2_results = model_2_results[:30]

from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

model_1_embeddings = model.encode(model_1_results, convert_to_tensor=True)
model_2_embeddings = model.encode(model_2_results, convert_to_tensor=True)
cosine_scores = util.cos_sim(model_1_embeddings, model_2_embeddings)
similarity_scores = torch.diag(cosine_scores)
scores_list = similarity_scores.tolist()

for i, score in enumerate(scores_list):
    print(f"Entries {i} with similarity score of {score:.6f}")