from openai import OpenAI
from dotenv import load_dotenv
import os

# Bloco de Código para pegar configurar a Key da OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


# Bloco de Codigo da Chamada na API apresentando a resposta
while True:
    # Bloco da Pergunta
    user_Input = input("\n>>>Digite uma pergunta para o Chat (Para encerrar: 'sair'): ")

    # Encerra o programa de Chat
    if user_Input.lower() == "sair":
        print("Chat encerrado!")
        break

    # Bloco de integracao com o ChatGPT
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Motor de busca
        messages=[{"role": "user", "content": user_Input}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
