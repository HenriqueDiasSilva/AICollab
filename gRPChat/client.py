import threading

import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc

from tkinter import *
from tkinter import simpledialog
from tkinter import font
from PIL import Image, ImageTk

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
            self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # Adiciona mensagem à interface

    def send_message(self, event):
        message = self.entry_message.get()
        if message != '':
            n = chat.Note()  
            n.name = self.username  
            n.message = message  
            self.conn.SendNote(n)  # Envia a mensagem para o servidor
            self.entry_message.delete(0, END) 

    def __setup_ui(self):
        self.window.title("AICollab")
        
        self.logo_image = Image.open("./img/logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(self.window, image=self.logo_photo)
        self.logo_label.pack(side=TOP)
        
        self.chat_list = Text(self.window, wrap=WORD)
        self.chat_list.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        
        custom_font = font.Font(family="Times New Roman", size=14)
        self.lbl_username = Label(self.window, text='User: ' + self.username, anchor=CENTER, font=custom_font)
        self.lbl_username.pack(side=TOP)
        
        self.entry_message = Entry(self.window, bd=5) 
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM, fill=X, padx=10, pady=10)

if __name__ == '__main__':
    root = Tk()
    root.geometry("600x600")
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("User", "Username:", parent=root)
    root.deiconify()
    c = Client(username, root)  # Inicia cliente e a thread que vai manter a conexão com o servidor aberta