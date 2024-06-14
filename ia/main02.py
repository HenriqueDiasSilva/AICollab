import requests
from dotenv import load_dotenv
import os
import json

# Carregar a chave da API do OpenAI
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

def perguntar_ao_chatgpt(pergunta):
    """
    Função que recebe uma pergunta e retorna a resposta do ChatGPT.

    Args:
        pergunta (str): A pergunta a ser feita ao ChatGPT.

    Returns:
        str: A resposta do ChatGPT.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": pergunta}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        resposta = response.json()
        return resposta['choices'][0]['message']['content']
    else:
        return f"Erro: {response.status_code} - {response.text}"

# Exemplo de uso da função
while True:
    user_Input = input("\n>>>Digite uma pergunta para o Chat(Digite 'sair' para encerrar): ")
    if user_Input.lower() == "sair":
        print("Chat encerrado!")
        break

    resposta = perguntar_ao_chatgpt(user_Input)
    print(resposta)
