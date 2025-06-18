'''

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


print(response)
