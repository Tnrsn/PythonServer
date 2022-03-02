import socket
import threading

PORT = 4545
HOST = socket.gethostbyname(socket.gethostname())

Disconnect_msg = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ADDR = (HOST, PORT)
server.bind(ADDR)
server.listen(1)


def handle_client(conn, addr):
    print(f"{ADDR} connected to server!")
    conn.send(bytes("Hello client", "utf-8"))
    connected = True
    while connected:
        msg = conn.recv(360).decode('utf-8')
        if msg:
            if msg == Disconnect_msg:
                    connected= False
            print(f"{addr} {msg}")

    conn.close()
    print(f"{ADDR} is diconnected")

def start():
    server.listen()
    print("Server is running...")
    while True:
        conn, ADDR = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, ADDR))
        thread.start()

print("Server is starting...")

start()