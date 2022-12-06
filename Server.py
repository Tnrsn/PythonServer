import socket
import threading

PORT = 4545
HOST = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ADDR = (HOST, PORT)
server.bind(ADDR)
server.listen(1)

conns = []


def handle_client(conn, addr):
    try:
        print(f"{addr} connected to server!")
        connected = True
        if connected:
            conn.send(bytes("Write your name:", "utf-8"))
            name = conn.recv(360).decode('utf-8')
            conns.append(conn)
            for c in conns:
                c.send(bytes(name + " joined to the server!", "utf-8"))

        while connected:
            msg = conn.recv(360).decode('utf-8')
            if msg:
                if msg[0] == '/':
                    if msg[1:8] == 'setname':
                        name = msg[9:]
                        conns[conns.index(conn)] = conn
                    elif msg[1: 6] == 'clear':
                        conn.send(bytes("exec subprocess.run('cls', shell=True)", "utf-8"))
                    elif msg[1: 9] == 'commands':
                        conn.send(bytes("-SERVER- Commands:\n1:  setname\n2:  clear", "utf-8"))
                    else:
                        conn.send(bytes("-SERVER- (Invalid Command)", "utf-8"))

                elif len(msg) < 80:
                    for c in conns:
                        if c == conn:
                            c.send(bytes('YOU (' + name + '): ' + msg, "utf-8"))
                        else:
                            c.send(bytes(name + ': ' + msg, "utf-8"))
                else:
                    conn.send(bytes("Message limit exceeded! Letter limit is 80", "utf-8"))
            

    except:
        for c in conns:
            if c != conn:
                c.send(bytes(f"{name} disconnected!", "utf-8"))
        conn.close()
        print(f"{addr} disconnected!")
        conns.remove(conn)



def start():
    server.listen()
    print("Server is running...")
    while True:
        conn, ADDR = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, ADDR))
        thread.start()


print("Server is starting...")

start()
