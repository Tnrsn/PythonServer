import socket

PORT = 4545

Disconnect_msg = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


def send_msg(msg):
    message = msg.encode('utf-8')
    client.send(message)


while True:
    msg = input()
    send_msg(msg)