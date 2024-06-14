import threading
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc
from tkinter import *
from tkinter import simpledialog
from tkinter import font
from PIL import Image, ImageTk

address = 'localhost'
port = 50052

class Client:

    def __init__(self, u: str, window):
        self.window = window
        self.username = u
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        # Enviando a mensagem de inicialização
        init_note = chat.Note()
        init_note.name = self.username
        init_note.message = ""
        try:
            for note in self.conn.ChatStream(init_note):
                self.display_message(note.name, note.message)
        except grpc.RpcError as e:
            print(f"Exception in __listen_for_messages: {e.code()} - {e.details()}")

    def display_message(self, name, message):
        self.chat_list.insert(END, f"[{name}] {message}\n")
        self.chat_list.see(END)  # Scroll até o final para mostrar a nova mensagem

    def send_message(self, event=None):
        message = self.entry_message.get()
        if message != '':
            n = chat.Note()
            n.name = self.username
            n.message = message
            print(f"Sending message: [{n.name}] {n.message}")
            self.conn.SendNote(n)
            self.entry_message.delete(0, END)

    def __setup_ui(self):
        self.window.title("AICollab")
        
        self.logo_image = Image.open("./img/logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = Label(self.window, image=self.logo_photo)
        self.logo_label.pack(side=TOP, pady=5)
        
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
    c = Client(username, root)
