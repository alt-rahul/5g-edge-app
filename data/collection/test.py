#the comments were getting out of hand so I'm starting a fresh file
from pymongo import MongoClient
from ollama import Client as OllamaClient
import json
from dotenv import load_dotenv, find_dotenv
import requests
from datetime import datetime
import os
import asyncio  


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
prompts = [
    # Math (10)
    "Calculate 14 + 27 and provide the numeric result.",
    "Compute 25% of 360 and state the answer.",
    "Solve for x in the equation 4x + 7 = 3x + 15, showing each step.",
    "Find the area of a circle with radius 5 units, using π ≈ 3.1416.",
    "Evaluate the definite integral ∫₀² (4x³ − 2x + 1) dx and give the exact value.",
    "Compute the eigenvalues of the matrix [[2,1],[1,2]] and explain your method.",
    "Prove by induction that for all n ≥ 1, 1³ + 2³ + ⋯ + n³ = (n(n+1)/2)².",
    "Determine all integer solutions (x, y) to the Diophantine equation x² − 3y² = 1.",
    "Outline a rigorous proof of the Prime Number Theorem in 500 words.",
    "Present and prove Galois’s fundamental theorem of Galois theory in at least 800 words.",
    # Science (10)
    "List the chemical symbols for hydrogen, oxygen, and carbon.",
    "Describe in one sentence what photosynthesis does in plants.",
    "Explain how enzymes function to lower activation energy in biochemical reactions (100 words).",
    "Describe the stages of the human cell cycle and their durations (150 words).",
    "Derive the ideal gas law PV = nRT from first principles of kinetic molecular theory (200 words).",
    "Explain the mechanism of DNA replication in eukaryotic cells, including major enzymes (250 words).",
    "Outline in detail the steps of the citric acid cycle, including intermediates and enzymes (300 words).",
    "Discuss the evidence supporting continental drift and plate tectonics theory (350 words).",
    "Explain the mathematical formulation of the Schrödinger equation and its physical interpretation (500 words).",
    "Describe how LIGO detects gravitational waves, including instrumentation and data analysis (600 words).",
    # Writing (10)
    "Write a 50-word descriptive paragraph about a peaceful forest scene.",
    "Compose a 100-word personal introduction for a professional networking profile.",
    "Draft a 300-word persuasive paragraph arguing for daily exercise benefits.",
    "Write a 400-word narrative about overcoming a significant challenge.",
    "Produce a 600-word analytical essay on the symbolism in Shakespeare’s 'Macbeth'.",
    "Compose a 700-word critical review of a recent scientific article of your choice.",
    "Write a 1000-word literature review on modern interpretations of Greek mythology.",
    "Draft a 1200-word research proposal on renewable energy technology adoption.",
    "Generate a 2000-word comprehensive thesis chapter on artificial intelligence ethics.",
    "Create a 5000-word comparative analysis of two major philosophical doctrines.",
    # Trivia (10)
    "Name the largest planet in our solar system.",
    "State the year the first man landed on the Moon.",
    "Identify the author of 'To Kill a Mockingbird' and the year it was published.",
    "Name the chemical element with atomic number 82 and its common use (100 words).",
    "List all continents in alphabetical order and give one unique fact about each (200 words).",
    "Identify the winner of the Nobel Prize in Literature in 2020 and summarize their work (250 words).",
    "Name the five longest rivers in the world and provide their approximate lengths (300 words).",
    "List the top ten highest-grossing films of all time and their release years (350 words).",
    "Detail the historical evolution of the Olympic Games from ancient Greece to the modern era (500 words).",
    "Describe the complete lineup of the Beatles and their roles, including years active (600 words).",
    # Programming (10)
    "Write a Python one-liner to reverse a string 'hello' and print the result.",
    "Explain in one paragraph what a 'for' loop does in programming.",
    "Implement a Python function `is_prime(n)` that returns True if n is prime, with comments.",
    "Write SQL to retrieve the top 5 highest-paid employees from an 'employees' table.",
    "Implement quicksort in Java, including partition and recursive calls, with inline comments.",
    "Write JavaScript code to implement a debounced function with a 300ms delay.",
    "Build a basic singly linked list in C++ with methods for insert, delete, and search.",
    "Compare and contrast REST and GraphQL APIs in a 400-word essay.",
    "Design and code a MapReduce job in pseudocode to count word frequency in a large text corpus (500 words).",
    "Describe the CAP theorem and implement a small simulated distributed key-value store in 600 words.",
    # Mixed (20)
    "List five prime numbers between 1 and 100.",
    "Spell the word 'pharaoh' correctly.",
    "State the boiling point of ethanol in Celsius.",
    "Name three branches of the United States government.",
    "Solve the system of equations: 2x + y = 5 and x − y = 1, showing steps.",
    "Explain Newton’s third law of motion with a real-world example (150 words).",
    "Write pseudocode for computing the factorial of a number using recursion.",
    "Identify the capital cities of France, Japan, and Brazil.",
    "Balance the chemical equation: C₃H₈ + O₂ → CO₂ + H₂O, and explain coefficients.",
    "Compare the themes of friendship in 'Of Mice and Men' and 'The Kite Runner' (200 words).",
    "Explain how blockchain consensus mechanisms work, focusing on Proof of Work (250 words).",
    "Write a regular expression that matches a valid IPv4 address and explain each part.",
    "Prove that there are infinitely many primes congruent to 1 mod 4 in 300 words.",
    "Analyze the economic causes of the 2008 financial crisis in 350 words.",
    "Design a RESTful API specification for a task management system (500 words).",
    "Explain the process of transcription and translation in gene expression (400 words).",
    "Discuss Gödel’s incompleteness theorems and their implications for mathematics (600 words).",
    "Outline the development of quantum computing hardware and current challenges (700 words).",
    "Implement a basic feedforward neural network forward pass in pseudocode with commentary (800 words).",
    "Critically evaluate Utilitarianism versus Kantian ethics in a 1000-word essay."
]
INITIAL_TIME = datetime.now()
INITIAL_TIME_STRING = INITIAL_TIME.strftime("%H:%M:%S")

mongo_connection_url = f"mongodb+srv://rr1437:{MY_PASSWORD}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
monogo_client = MongoClient(mongo_connection_url)
mongo_db = monogo_client['dataset']
mongo_col = mongo_db['ollama']

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
        print("\nStaring task...\n")
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