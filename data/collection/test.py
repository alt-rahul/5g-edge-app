#the comments were getting out of hand so I'm starting a fresh file
from pymongo import MongoClient
from ollama import Client as OllamaClient
import json
from dotenv import load_dotenv, find_dotenv
import requests
from datetime import datetime
import os
import asyncio  
from prompts import prompts

load_dotenv(find_dotenv())
MY_PASSWORD = os.environ.get("RAHUL_PASS")
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
OLLAMA_URL = 'http://localhost:11434'
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

prompts = prompts
INITIAL_TIME = datetime.now()
INITIAL_TIME_STRING = INITIAL_TIME.strftime("%H:%M:%S")

mongo_connection_url = f"mongodb+srv://rr1437:{MY_PASSWORD}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
monogo_client = MongoClient(mongo_connection_url)
mongo_db = monogo_client['dataset']
mongo_col = mongo_db['mega2']

ollama_client = OllamaClient(
    host=OLLAMA_URL,
)

def fetch_intial_metrics():
    intial_doc = {}
    print("Initializing Stationary Metrics...\n")
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
    intial_doc["Category"] = "Initial"

    mongo_col.insert_one(intial_doc)
    print('Finished Collecting Initial Metrics...\n')
    return intial_doc

async def fetch_verbose(prompt):
    print(f"Sending a prompt to Ollama...\n")
    def block_call():
        return ollama_client.chat(model='llama3.1:8b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
    response = await asyncio.to_thread(block_call)
    response = response.model_dump_json()
    response = json.loads(response)
    response['prompt_eval_rate'] = f"{response['prompt_eval_count']/(response['prompt_eval_duration'] /(10**9))} tokens/s"
    response['eval_rate'] = f"{response['eval_count']/(response['eval_duration'] /(10**9))} tokens/s"
    response.pop('done_reason')
    now = datetime.now()
    response["Current Time"] = now.strftime("%H:%M:%S")

    print(f"\nSuccessfully Requested Ollama Prompt...\n")
    return response

def fetch_live_metrics(num, count):
    live_doc = { }
    for metric_name, metric_query in LIVE_METRICS.items():
        response = requests.get(PROMETHEUS_URL, params={"query":metric_query})
        results = response.json()
        result = results["data"]["result"][0]["value"][1]        
        live_doc[metric_name] = float(result)

    now = datetime.now()
    timedelta = now - INITIAL_TIME
    live_doc ["Current Time"]  = now.strftime("%H:%M:%S")
    live_doc["Time Delta"] = timedelta.seconds
    live_doc['Category'] = f"Prompt {num}"
    live_doc['Iteration'] = count
    print(f"Finished Collecting Metric #{count}...")
    mongo_col.insert_one(live_doc)
    return live_doc

async def main():
    fetch_intial_metrics()
    for num, prompt in enumerate(prompts):
        print(f"\nOn Prompt {num}: Staring task...\n")
        task = asyncio.create_task(fetch_verbose(prompt))
        count = 0
        while not task.done():
            count +=1
            await asyncio.to_thread(fetch_live_metrics, num, count)
        answer = await task
        mongo_col.insert_one(answer)
        print("\nFinished task...\n")
        print("--------------")

asyncio.run(main())