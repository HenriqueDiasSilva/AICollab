import pathlib
import textwrap
from dotenv import load_dotenv
import os
import google.generativeai as genai


model = genai.GenerativeModel('gemini-1.0-pro-latest')

load_dotenv()
APIKEY = os.getenv('apiKey01')
genai.configure(api_key=APIKEY)

def prompt():
    while True:
        # Perguntar ao usuário sua pergunta
        pergunta = input("Faça sua pergunta para o Bard: ")

        # Enviar a pergunta para o Bard e obter a resposta
        resposta = model.generate_content(pergunta)

        # Imprimir a resposta do Bard
        if resposta:
            print(f"Bard: {resposta.text}")
        else:
            print("Erro ao obter resposta do Bard.")

prompt()