'''
(Will probably move back to `script.py`) This makes sure we can easily attain performace
metrics of the LLM that we'll use to consider in the benchmarks.
'''

from ollama import Client
client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='deepseek-r1', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

response = response.model_dump_json()

print(response)

