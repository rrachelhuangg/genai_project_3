## GenAI Project 3 - Rachel Huang



## Data Compilation and Analysis: Prompt Engineering for In-Context Learning
This project explores the power of in-context learning by designing effective prompts to perform various software engineering tasks. Implements different prompting strategies for a diverse set of problems using large language models (LLM's). 
* Models used:
  * OpenAI's gpt-4o
  * Google Gemini 2.0 Flash
  * Ollama llava:7b-v1.6
  * Mistral's Large-Latest
* Prompt Engeering Strategies used:
  * Zero Shot
  * Few Shot
  * Chain-of-Thought
  * Self-Consistency
  * Prompt Chaining

These strategies are applied to 22 software engineering tasks that are each tested on two models. Various combinations of stratgies and models were applied to the tasks, specifically:
* First five tasks: Zero shot, few shot + Gemini, Ollama
* Next five tasks: Zero shot, few shot + Gemini, GPT-4o
* Next five tasks: Few Shot, Chain of Thought + GPT-4o, Ollama
* Next five tasks: Prompt Chaining, Self-Consistency + Gemini, Mistral
* Last two tasks (extra-credit): Chain of Thought, Self-Consistency + Gemini, Mistral

## Implementation of Results Compilation and Data Analysis Pipeline
Collection of data results were automated by `pipe_1.py`, `pipe_2.py`, `pipe_3.py`, `generate_prompts.py`, `mistral.py`, and `self_consistency.py`. Pipe_1 completely automated the testing and results collection of the first five tasks, writing the results into the subset_1 directory files. Pipe_2 automated the testing and results collection of the next five tasks, writing the results into the subset_2 directory files. Pipe_3 automated the testing and results collection of the next five tasks, writing the results into the subset_3 directory files. The remaining highlighted files were used for the remaining tasks in various combinations to collect the necessary results. 

Cosine-vector similarity analysis was applied to the CodeT5 embeddings of the above results that were stored in `Results_Report.xslx`. The vector embedding and cosine similarity analysis was automated with `calc_vec_score.py`. 

## Testing
* `git clone https://github.com/rrachelhuangg/genai_project_3.git`
* `cd genai_project_3`
* `python -m venv .venv`
* `source .venv/bin/activate`
* `pip install requirements.txt`
* Can run `python pipe_1.py` for a demo of the testing and results extraction to subset_1 directory. 

## Viewing Results Report/Datasets
`Results_Report.xslx` contains all of the prompts used, with the corresponding combinations of strategies and models applied to each of the 22 tasks. A written analysis of each task's result is also included in the `Analysis` column of the spreadsheet. [written report, etc.]
