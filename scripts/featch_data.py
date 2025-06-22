import pymongo 
from pymongo import MongoClient
import os 
from dotenv import load_dotenv, find_dotenv
import numpy as np
import pandas as pd

load_dotenv(find_dotenv())
my_password = os.environ.get("RAHUL_PASS")

documents = {}

try: 
    uri = f"mongodb+srv://rr1437:{my_password}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
    client = MongoClient(uri)

    database = client["main"]
    collection = database["test_gpu_metrics"]

    results = collection.find({"Time Delta" : 0})

    for result in results:
        for key, value in result.items():
            documents[key] = value

    client.close()


except Exception as e:
    raise Exception(
        "Recieved the following error:" + e
    )


# documents = pd.DataFrame(documents)
# documents.head()
# print(documents)