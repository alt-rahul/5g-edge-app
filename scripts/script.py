'''
This code connects to MongoDB cluster, fetches specific metrics from local Prometheus API 
and sends them to the cluster. 
'''

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
og_db = client['main']
og_col = og_db['test_gpu_metrics']


#because we're using prometheus locally (set up local ports using orobit) we're 
#fetching metric info from the following api
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"


#metrics we only would need to collect once 
INITIAL_METRICS = {
    'Power Limit (Watts)': 'nvidia_smi_power_default_limit_watts', 
    "Memory Clock Limit (MHz)":'nvidia_smi_clocks_max_memory_clock_hz', 
    'Total Memory Allocation (MB)':"nvidia_smi_memory_total_bytes", 
    "GPU Clock Limit (MHz)":'nvidia_smi_clocks_max_graphics_clock_hz',
    "GPU Info": ""
}

#these are all the metrics we'll be collecting from prometheus
LIVE_METRICS = {
    "GPU Utilization (%)": 'nvidia_smi_utilization_gpu_ratio',
    "Power Draw (Watts)": 'nvidia_smi_power_draw_watts',    
    "GPU Temp (°C)":'nvidia_smi_temperature_gpu',
    "GPU Current Clock (MHz)":'nvidia_smi_clocks_current_graphics_clock_hz',
    "Memory Current Clock (MHz)":'nvidia_smi_clocks_current_memory_clock_hz',
    'Memory Allocation Used (MB)':"nvidia_smi_memory_used_bytes",
    'Memory Utilization (%)':"nvidia_smi_utilization_memory_ratio",
}

INITAL_TIME = datetime.now()
INTIAL_TIME_STRING = INITAL_TIME.strftime("%H:%M:%S")


doc = {}

def fetch_intial_metrics():
    intial_doc = {}
    for metric_name, metric_query in INITIAL_METRICS.items():
        response = (requests.get(url=PROMETHEUS_URL, params={'query':metric_query})).json()
        response = response['data']["result"][0]["value"][1]
        intial_doc[metric_name] = response
    intial_doc['Start Time'] = INTIAL_TIME_STRING



count = 0

def fetch_metrics():
    doc = { }
    for metric_name, metric_query in metrics.items():
        response = requests.get(PROMETHEUS_URL, params={'query':metric_query})
        results = response.json()
        result = results['data']['result'][0]['value'][1]        
        doc[metric_name] = float(result)
    
    response = requests.get(PROMETHEUS_URL, params={"query":QUERY})
    response = response.json()
    doc['GPU Info'] = response['data']['result'][0]['metric']['name']
    
    doc["Start Time"] = time_string
    now = datetime.now()
    timedelta = now - initial
    doc ['Current Time']  = now.strftime("%H:%M:%S")
    doc['Time Delta'] = timedelta.seconds
    
    doc["Test Stage"] = curr_stage
    
    og_col.insert_one(doc)
    print(f"Finished Collecting Collection #{count + 1}")
    

while(True):
    fetch_metrics()
    time.sleep(1)
    count+=1




