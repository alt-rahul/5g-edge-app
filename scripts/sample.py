import requests 

api_url = "https:localhost:9090/api/v1"

QUERY = "nvidia_smi_gpu_info"

response = requests.get(url=api_url, params={"query":QUERY})

response = response.json()

print(response)

