from concurrent import futures
import grpc
import time
import requests

import chat_pb2 as chat
import chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):  

    def __init__(self):
        self.chats = []
        
    def ChatStream(self, request_iterator, context):
        """
        Esse é um stream de resposta. Isso significa que o servidor pode continuar mandando mensagens.
        Todo cliente abre essa conexão e espera pelo servidor mandar novas mensagens.
        """
        lastindex = 0

        while True:
            # Verifica possíveis novas mensagens
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        """
        Esse método é chamado quando um cliente envia uma mensagem para o servidor.
        """
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)

        # Enviar a mensagem recebida para a API de chat
        url = "http://localhost:11434/api/chat"
        data = {
            "model": "phi3",
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            "stream": False
        }

        response = requests.post(url, json=data)

        # Verificar a resposta da API
        if response.status_code == 200:
            json_response = response.json()
            message_content = json_response.get('message', {}).get('content', '')
            if message_content:
                # Criar uma nova Note com a resposta da API
                response_note = chat.Note(
                    name="server",
                    message=message_content
                )
                # Adicionar a resposta na lista de chats
                self.chats.append(response_note)
        else:
            print("Failed to get a valid response from the API. Status Code:", response.status_code)

        return chat.Empty()

if __name__ == '__main__':
    port = 50051 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # Cria um servidor gRPC que aceita no máximo 10 conexões
    rpc.add_ChatServerServicer_to_server(ChatServer(), server) 
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    # O servidor inicia em segundo plano (em outro thread), então continua aguardando
    # se o tempo de espera não for criado, a thread main vai se encerrar, e por consequência, todas as demais
    while True:
        time.sleep(64 * 64 * 100)
