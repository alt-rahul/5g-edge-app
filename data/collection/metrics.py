"""
This code connects to MongoDB cluster, fetches specific metrics from local Prometheus API 
and sends them to the cluster. 
"""

import requests
import time
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
from datetime import datetime

# so here we're just doing some basic dotenv imports to get our db password
load_dotenv(find_dotenv())
my_password = os.environ.get("RAHUL_PASS")

# actually connecting our MongoDB database 
connection_string = f"mongodb+srv://rr1437:{my_password}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
client = MongoClient(connection_string)
# print(client.list_database_names())

#filtering client into our specific database and collection
og_db = client["main"]
og_col = og_db["init_stage"]

#because we're using prometheus locally (set up local ports using orobit) we're 
#fetching metric info from the following api
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"


#metrics we only would need to collect once 
INITIAL_METRICS = {
    "Power Limit (Watts)": "nvidia_smi_power_default_limit_watts", 
    "Memory Clock Limit (MHz)":"nvidia_smi_clocks_max_memory_clock_hz", 
    "Total Memory Allocation (MB)":"nvidia_smi_memory_total_bytes", 
    "GPU Clock Limit (MHz)":"nvidia_smi_clocks_max_graphics_clock_hz",
    "GPU Info": "nvidia_smi_gpu_info"
}

#these are all the metrics we"ll be collecting from prometheus
LIVE_METRICS = {
    "GPU Utilization (%)": "nvidia_smi_utilization_gpu_ratio",
    "Power Draw (Watts)": "nvidia_smi_power_draw_watts",    
    "GPU Temp (°C)":"nvidia_smi_temperature_gpu",
    "GPU Current Clock (MHz)":"nvidia_smi_clocks_current_graphics_clock_hz",
    "Memory Current Clock (MHz)":"nvidia_smi_clocks_current_memory_clock_hz",
    "Memory Allocation Used (MB)":"nvidia_smi_memory_used_bytes",
    "Memory Utilization (%)":"nvidia_smi_utilization_memory_ratio",
}

INITAL_TIME = datetime.now()
INTIAL_TIME_STRING = INITAL_TIME.strftime("%H:%M:%S")


def fetch_intial_metrics():
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

    intial_doc["Start Time"] = INTIAL_TIME_STRING
    intial_doc["Status"] = "Initial"
    og_col.insert_one(intial_doc)

count = 1

def fetch_metrics():
    live_doc = { }
    for metric_name, metric_query in LIVE_METRICS.items():
        response = requests.get(PROMETHEUS_URL, params={"query":metric_query})
        results = response.json()
        result = results["data"]["result"][0]["value"][1]        
        live_doc[metric_name] = float(result)
    
    if live_doc['GPU Utilization (%)'] > 80:
        live_doc['GPU Stress'] = 'On'
    else:
        live_doc['GPU Stress'] = 'Off'    
    
    now = datetime.now()
    timedelta = now - INITAL_TIME
    live_doc ["Current Time"]  = now.strftime("%H:%M:%S")
    live_doc["Time Delta"] = timedelta.seconds
    live_doc['Status'] = "Live"
    live_doc['Iteration'] = count
    print(f"Finished Collecting Collection #{count}")
    og_col.insert_one(live_doc)

fetch_intial_metrics()
while(True):
    fetch_metrics()
    time.sleep(1)
    count+=1




