from concurrent import futures

import grpc
import time

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
