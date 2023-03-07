import socket
import threading
# set up the port and host
PORT = 4545
HOST = socket.gethostbyname(socket.gethostname())
# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket object to the specified address
ADDR = (HOST, PORT)
server.bind(ADDR)
# listen for incoming connections on the specified port
server.listen(1)
# list to hold all connected clients
conns = []
# function to handle each client
def handle_client(conn, addr):
    try:
        # indicate that a client has connected
        print(f"{addr} connected to server!")
        # set flag to indicate client is connected
        connected = True
        # send prompt to client to enter their name
        if connected:
            conn.send(bytes("Write your name:", "utf-8"))
            # receive client's name and decode it
            name = conn.recv(360).decode('utf-8')
            # add the client's connection to the list of connections
            conns.append(conn)
            # send message to all connected clients that a new client has joined
            for c in conns:
                c.send(bytes(name + " joined to the server!", "utf-8"))
        # loop to handle client messages
        while connected:
            # receive message from client and decode it
            msg = conn.recv(360).decode('utf-8')
            if msg:
                # if message starts with '/', it is a command
                if msg[0] == '/':
                    # if command is 'setname', change the client's name
                    if msg[1:8] == 'setname':
                        name = msg[9:]
                        # update client's connection in list of connections
                        conns[conns.index(conn)] = conn
                    # if command is 'commands', list available commands
                    elif msg[1: 9] == 'commands':
                        conn.send(bytes("-SERVER- Commands:\n1:  setname", "utf-8"))
                    # otherwise, send invalid command message to client
                    else:
                        conn.send(bytes("-SERVER- (Invalid Command)", "utf-8"))
                # if message is not a command and is less than 80 characters, send to all clients
                elif len(msg) < 80:
                    for c in conns:
                        if c == conn:
                            c.send(bytes('YOU (' + name + '): ' + msg, "utf-8"))
                        else:
                            c.send(bytes(name + ': ' + msg, "utf-8"))
                # if message is longer than 80 characters, send message limit exceeded message to client
                else:
                    conn.send(bytes("Message limit exceeded! Letter limit is 80", "utf-8"))
    except:
        # if an error occurs, send disconnect message to other clients and remove client's connection from list
        for c in conns:
            if c != conn:
                c.send(bytes(f"{name} disconnected!", "utf-8"))
        conn.close()
        # indicate that the client has disconnected
        print(f"{addr} disconnected!")
        conns.remove(conn)
# function to start the server and listen for incoming connections
def start():
    # start listening for incoming connections
    server.listen()
    # indicate that the server is running
    print("Server is running...")
    # loop to handle incoming connections
    while True:
        # accept incoming connection and create a new thread to handle it
        conn, ADDR = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, ADDR))
        thread.start()
print("Server is starting...")
#initilaizes the server
start()