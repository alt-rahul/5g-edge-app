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
print(client.list_database_names())

#filtering client into our specific database and collection
og_db = client['main']
og_col = og_db['gpu_metrics']


#because we're using prometheus locally (set up local ports using orobit) we're 
#fetching metric info from the following api
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"


#this was our sample query - (like bro this is like not even that much work fr fr)
QUERY = 'nvidia_smi_utilization_gpu_ratio'

#these are all the metrics we'll be collecting from prometheus
metrics = {
    "GPU Utilization": 'nvidia_smi_utilization_gpu_ratio',
    "Power Draw": 'nvidia_smi_power_draw_watts',
    'Power Limit': 'nvidia_smi_power_default_limit_watts',
    "GPU Temp":'nvidia_smi_temperature_gpu',
    "GPU Current Clock":'nvidia_smi_clocks_current_graphics_clock_hz',
    "GPU Clock Limit":'nvidia_smi_clocks_max_graphics_clock_hz',
    "Memory Current Clock":'nvidia_smi_clocks_current_memory_clock_hz',
    "Memory Clock Limit":'nvidia_smi_clocks_max_memory_clock_hz',
    'Memory Allocation Used':"nvidia_smi_memory_used_bytes",
    'Memory Allocation Total':"nvidia_smi_memory_total_bytes",
    'Memory Utilization (VRAM)':"nvidia_smi_utilization_memory_ratio",
}


#function for fetching all the metrics (request each one by one) and then structing the metrics into a dictionary
#that we insert into as a single observation or data point into MongoDB
def fetch_metrics():
    doc = { }
    for metric_name, metric_query in metrics.items():
        response = requests.get(PROMETHEUS_URL, params={'query':metric_query})
        results = response.json()
        result = results['data']['result'][0]['value'][1]        
        doc[metric_name] = result
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    doc["time"] = time_string
    og_col.insert_one(doc)
    print("Finished Collecting One Collection")
    

while(True):
    fetch_metrics()
    time.sleep(10)




