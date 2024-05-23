import requests

# Definindo a URL base do servidor e o endpoint
url = "http://localhost:11434/api/chat"

# Definindo os dados a serem enviados na requisição
data = {
    "model": "phi3",
    "messages": [
        {
            "role": "user",
            "content": "Why is the sky blue?"
        }
    ],
    "stream": False
}

# Fazendo a requisição POST
response = requests.post(url, json=data)

# Verificando a resposta
if response.status_code == 200:
    json_response = response.json()    
    # Processar a resposta JSON conforme necessário
    message = json_response.get('message', {})
    content = message.get('content', '')
    print(content)
else:
    print("Failed to get a valid response. Status Code:", response.status_code)
