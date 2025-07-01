'''
(Will probably move back to `script.py`) This makes sure we can easily attain performace
metrics of the LLM that we'll use to consider in the benchmarks.
'''

from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
from ollama import Client
import json

prompts = [
    "Summarize each chapter of ‘War and Peace’ in sequence, and then write a 500-word synthesis of the overall themes.",
    "Act as a code reviewer. I’ll paste a large codebase. Review each file, list issues, and then provide an overall review.",
    "Create a research paper with citations on the effects of climate change on marine biodiversity. First, outline, then write each section.",
    # "Simulate a roundtable debate between five philosophers (e.g., Kant, Nietzsche, Confucius, etc.) on AI ethics. Include 3 turns per character.",
    # "Write a 5,000-word fantasy short story including a hero’s journey, detailed magic system, and three named civilizations with cultures.",
    # "Generate a novel chapter-by-chapter plot for a mystery thriller. Then write a draft of chapter one.",
    # "Create documentation for a new programming language with sample code, tutorials, and API references.",
    # "Generate 100 unique product descriptions for fictional gadgets, each with a catchy name, spec sheet, and marketing slogan.",
    # "Simulate a text-based game engine with inventory, combat, and dialogue. Write the core logic and run a 5-turn playthrough.",
    # "Build a full-stack app mockup: frontend design, backend API, and sample database. Include comments and tests.",
    # "Generate a markdown-based static site with 10 interlinked pages, including CSS styling, based on a fictional museum.",
    # "Plan a Mars colonization mission: break down tech requirements, stages, risks, costs, and timeline over 20 years.",
    # "Reverse engineer a user manual from a list of features and use cases of a fictional drone model.",
    # "Analyze the political implications of AGI in 2050 from the perspectives of the US, China, EU, and UN.",
    # "Design a curriculum for a 3-month bootcamp to train LLM prompt engineers. Include weekly topics and exercises."
]

load_dotenv(find_dotenv())
my_password = os.environ.get("RAHUL_PASS")

connection_string = f"mongodb+srv://rr1437:{my_password}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
mongo_client = MongoClient(connection_string)

db = mongo_client['main']
col = db['verbose_test']


ollama_client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)

def gen_prompt(prompt):
  response = ollama_client.chat(model='llama3.1:8b', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
  response = response.model_dump_json()
  response = json.loads(response)
  response['prompt_eval_rate'] = f"{response['prompt_eval_count']/(response['prompt_eval_duration'] /(10**9))} tokens/s"
  response['eval_rate'] = f"{response['eval_count']/(response['eval_duration'] /(10**9))} tokens/s"
  response.pop('done_reason')
  print('response')
  return response

for prompt in prompts:
  return_response = gen_prompt(prompt)
  col.insert_one(return_response)



