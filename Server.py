import socket
import threading

# Set up the port and host
PORT = 4545
HOST = socket.gethostbyname(socket.gethostname())

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket object to the specified address
ADDR = (HOST, PORT)
server.bind(ADDR)

# Listen for incoming connections on the specified port
server.listen(1)

# List to hold all connected clients
conns = []

# Checks if the entered value is empty
def name_control(name):
    control = True
    if name == '':
        control = False
    if len(name) > 0:
        for item in name:
            if item == " ":
                control = False
    return control

# Function to handle each client
def handle_client(conn, addr):
    try:
        # Indicate that a client has connected
        print(f"{addr} connected to server!")
        # Set flag to indicate client is connected
        connected = True
        # Send prompt to client to enter their name
        if connected:
            conn.send(bytes("Write your name:", "utf-8"))
            # Receive client's name and decode it
            name = conn.recv(360).decode('utf-8')
            # Add the client's connection to the list of connections
            conns.append(conn)
            # Send message to all connected clients that a new client has joined
            for c in conns:
                c.send(bytes(name + " joined to the server!", "utf-8"))
        # Loop to handle client messages
        while connected:
            # Receive message from client and decode it
            msg = conn.recv(360).decode('utf-8')
            if msg:
                # If message starts with '/', it is a command
                if msg[0] == '/':
                    # If command is 'setname', change the client's name
                    if msg[1:8] == 'setname':
                        name = msg[9:]
                        # If name is not null write new name
                        if name_control(name):
                            # Update client's connection in list of connections
                            conns[conns.index(conn)] = conn
                            conn.send(bytes('Your new name is ' + name + '', "utf-8"))
                        # If name is null write error message
                        else:
                            conn.send(bytes("Enter a real name with the /setname command!", "utf-8"))
                    # If command is 'commands', list available commands
                    elif msg[1:9] == 'commands':
                        conn.send(bytes("-SERVER- Commands:", "utf-8"))
                        conn.send(bytes("1: setname", "utf-8"))
                    # Otherwise, send invalid command message to client
                    else:
                        conn.send(bytes("-SERVER- (Invalid Command)", "utf-8"))
                # If message is not a command and is less than 80 characters, send to all clients
                elif len(msg) < 80:
                    # If name is not null write message
                    if name_control(name):
                        for c in conns:
                            if c == conn:
                                c.send(bytes('YOU (' + name + '): ' + msg, "utf-8"))
                            else:
                                c.send(bytes(name + ': ' + msg, "utf-8"))
                # If message is longer than 80 characters, send message limit exceeded message to client
                else:
                    conn.send(bytes("Message limit exceeded! Letter limit is 80", "utf-8"))
    except:
        # If an error occurs, send disconnect message to other clients and remove client's connection from list
        for c in conns:
            if c != conn:
                c.send(bytes(f"{name} disconnected!", "utf-8"))
        conn.close()
        # Indicate that the client has disconnected
        print(f"{addr} disconnected!")
        conns.remove(conn)

# Function to start the server and listen for incoming connections
def start():
    # Start listening for incoming connections
    server.listen()
    # Indicate that the server is running
    print("Server is running...")
    # Loop to handle incoming connections
    while True:
        # Accept incoming connection and create a new thread to handle it
        conn, ADDR = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, ADDR))
        thread.start()

print("Server is starting...")
#Initilaizes the server
start()
