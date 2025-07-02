#the comments were getting out of hand so I'm starting a fresh file

from pymongo import MongoClient
from ollama import Client as OllamaClient
import json
from dotenv import load_dotenv, find_dotenv
import requests
import datetime
import os


load_dotenv(find_dotenv())
MY_PASSWORD = os.environ.get("RAHUL_PASS")
PROMETHEUS_URL = 'https://localhost:9090'
OLLAMA_URL = 'https://localhost:11434'
INITIAL_METRICS = {
    "Power Limit (Watts)": "nvidia_smi_power_default_limit_watts", 
    "Memory Clock Limit (MHz)":"nvidia_smi_clocks_max_memory_clock_hz", 
    "Total Memory Allocation (MB)":"nvidia_smi_memory_total_bytes", 
    "GPU Clock Limit (MHz)":"nvidia_smi_clocks_max_graphics_clock_hz",
    "GPU Info": "nvidia_smi_gpu_info"
}
LIVE_METRICS = {
    "GPU Utilization (%)": "nvidia_smi_utilization_gpu_ratio",
    "Power Draw (Watts)": "nvidia_smi_power_draw_watts",    
    "GPU Temp (°C)":"nvidia_smi_temperature_gpu",
    "GPU Current Clock (MHz)":"nvidia_smi_clocks_current_graphics_clock_hz",
    "Memory Current Clock (MHz)":"nvidia_smi_clocks_current_memory_clock_hz",
    "Memory Allocation Used (MB)":"nvidia_smi_memory_used_bytes",
    "Memory Utilization (%)":"nvidia_smi_utilization_memory_ratio",
}
prompts = [
    "Summarize each chapter of ‘War and Peace’ in sequence, and then write a 500-word synthesis of the overall themes.",
    "Act as a code reviewer. I’ll paste a large codebase. Review each file, list issues, and then provide an overall review.",
    "Create a research paper with citations on the effects of climate change on marine biodiversity. First, outline, then write each section.",
    "Simulate a roundtable debate between five philosophers (e.g., Kant, Nietzsche, Confucius, etc.) on AI ethics. Include 3 turns per character.",
    "Write a 5,000-word fantasy short story including a hero’s journey, detailed magic system, and three named civilizations with cultures.",
    "Generate a novel chapter-by-chapter plot for a mystery thriller. Then write a draft of chapter one.",
    "Create documentation for a new programming language with sample code, tutorials, and API references.",
    "Generate 100 unique product descriptions for fictional gadgets, each with a catchy name, spec sheet, and marketing slogan.",
    "Simulate a text-based game engine with inventory, combat, and dialogue. Write the core logic and run a 5-turn playthrough.",
    "Build a full-stack app mockup: frontend design, backend API, and sample database. Include comments and tests.",
    "Generate a markdown-based static site with 10 interlinked pages, including CSS styling, based on a fictional museum.",
    "Plan a Mars colonization mission: break down tech requirements, stages, risks, costs, and timeline over 20 years.",
    "Reverse engineer a user manual from a list of features and use cases of a fictional drone model.",
    "Analyze the political implications of AGI in 2050 from the perspectives of the US, China, EU, and UN.",
    "Design a curriculum for a 3-month bootcamp to train LLM prompt engineers. Include weekly topics and exercises."
]
INITIAL_TIME = datetime.now()
INITIAL_TIME_STRING = INITIAL_TIME.strftime("%H:%M:%S")


mongo_connection_url = f"mongodb+srv://rr1437:{MY_PASSWORD}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
monogo_client = MongoClient(mongo_connection_url)
mongo_db = monogo_client['main']
mongo_col = mongo_db['verbose_and_metrics']

ollama_client = OllamaClient(
    host=OLLAMA_URL,
)

mongo_col.insert_one({"Initial":"hello"})


def fetch_intial_metrics():
    query = {"Initial":"hello"}
    intial_doc = {}
    for metric_name, metric_query in INITIAL_METRICS.items():
        if metric_name == 'GPU Info':
            response = (requests.get(url=PROMETHEUS_URL, params={"query":metric_query})).json()
            response = response["data"]["result"][0]['metric']['name']
            intial_doc[metric_name] = response
        else:
            response = (requests.get(url=PROMETHEUS_URL, params={"query":metric_query})).json()
            response = float(response["data"]["result"][0]["value"][1])
            intial_doc[metric_name] = response        

    intial_doc["Start Time"] = INITIAL_TIME_STRING
    intial_doc["Status"] = "Initial"

    intial_doc = {"$set":{"Initial":intial_doc}}
    mongo_col.update_one(query, intial_doc)


for prompt in prompts:
    




