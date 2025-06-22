import pymango 
from pymango import MongoClient
import os 
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
my_password = os.environ.get("RAHUL_PASS")


try: 
    uri = f"mongodb+srv://rr1437:{my_password}@prometrics.h105zsq.mongodb.net/?retryWrites=true&w=majority&appName=ProMetrics"
    client = MongoClient(uri)

    database = client["ProMetrics"]
    collection = database["test_gpu_metrics"]

    client.close()

except Exception as e:
    raise Exception(
        "Recieved the following error:" + e
    )