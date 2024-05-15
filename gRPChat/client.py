import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
port = 50051


class Client:

    def __init__(self, u: str, window):
        # Frame para adicionar componentes da interface
        self.window = window
        self.username = u
        # gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        
        threading.Thread(target=self.__listen_for_messages, daemon=True).start() # Cria uma nova thread para ficar cuidando das novas mensgens que virão
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        for note in self.conn.ChatStream(chat.Empty()):  # Esperando por novas mensagens
            print("R[{}] {}".format(note.name, note.message))  
            self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # Adiciona mensagem à interface

    def send_message(self, event):
        message = self.entry_message.get() 
        if message is not '':
            n = chat.Note()  
            n.name = self.username  
            n.message = message  
            print("S[{}] {}".format(n.name, n.message))  
            self.conn.SendNote(n)  # Envia a mensagem para o servidor

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()  
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("User", "Nome de usuário:", parent=root)
    root.deiconify() 
    c = Client(username, frame)  # Inicia cliente e a thread que vai manter a conexão com o servidor aberta
