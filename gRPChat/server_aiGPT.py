import grpc
from concurrent import futures
import chat_pb2 as chat
import chat_pb2_grpc as rpc
from ia.main02 import perguntar_ao_chatgpt  # Importa a função para chamar a OpenAI

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.messages = []

    def ChatStream(self, request, context):
        user = request.name
        print(f"User connected: {user}")

        last_index = 0

        while True:
            while len(self.messages) > last_index:
                n = self.messages[last_index]
                last_index += 1
                yield n

    def SendNote(self, request, context):
        print(f"Received message from {request.name}: {request.message}")
        self.messages.append(request)
        
        # Se a mensagem começar com @chat, faça a pergunta ao ChatGPT
        if request.message.startswith("@chat"):
            user_input = request.message[len("@chat "):]
            response = perguntar_ao_chatgpt(user_input)
            new_note = chat.Note()
            new_note.name = "AI"
            new_note.message = response
            self.messages.append(new_note)
            print(f"AI response: {response}")
        
        return chat.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print('Starting server. Listening on port 50052.')
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
