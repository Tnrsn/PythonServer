import socket
import threading

PORT = 4545

Disconnect_msg = "!DISCONNECT"
#Server = "10.1.55.12"
SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


def send_msg():
    msg = input()
    message = msg.encode('utf-8')
    client.send(message)

def recieveMsg():
    print(client.recv(1024).decode())

while True:
    recieveThread = threading.Thread(target=recieveMsg, args=())
    sendThread = threading.Thread(target=send_msg, args=())
    recieveThread.start()
    sendThread.start()
