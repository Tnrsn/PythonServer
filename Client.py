import socket
import threading
import tkinter as tk

root = tk.Tk()
root.title("TApp")
root.geometry('800x600')
root.configure(bg='#212121')

# Create a Tkinter Listbox widget to display received messages
messageBox = tk.Listbox(root, width=80, height=15, bg='#303030', fg='white', borderwidth=0, font=("default", 15))
messageBox.pack(padx=20, pady=(20, 0), fill=tk.BOTH, expand=True)

# Create a Tkinter Entry widget for the user to enter messages
entry = tk.Entry(root, bg='#424242', fg='white', borderwidth=0, font=("default", 12), width=50)
entry.pack(side=tk.LEFT, padx=(20, 0), pady=(3, 10), fill=tk.BOTH, expand=True)

PORT = 4545 # Listening port
SERVER = socket.gethostbyname(socket.gethostname()) # Get the IP address of the local machine for debugging

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object for the client
client.connect((SERVER, PORT)) # Connect the client socket to the server socket

# Function to send messages to the server
def send_msg(event=None):
    msg = entry.get() # Get the message entered by the user
    entry.delete(0, "end") # Clear the input field
    message = msg.encode('utf-8') # Convert the message to bytes
    client.send(message) # Send the message to the server

# Function to clear the messageBox widget
def clear_msg(event=None):
    messageBox.delete(0, 'end')

# Function to receive messages from the server
def receive_msg():
    while True:
        try:
            # Receive a message from the server
            received_msg = client.recv(1024).decode()
            # Add the message to the messageBox widget
            messageBox.insert(tk.END, received_msg)
        except:
            # If an exception occurs, display an error message in the messageBox widget
            messageBox.insert(tk.END, "Disconnected from the server!")

# Bind the "Return" (aka "Enter") key to the send_msg function
entry.bind("<Return>", send_msg)

# Create a Tkinter Button widget to send messages
button = tk.Button(root, text="Submit", command=send_msg, bg='#00BFFF', fg='white', borderwidth=0, padx=1, pady=1, font=("default", 12))
button.pack(side=tk.LEFT, padx=(0, 20), pady=(3, 10), fill=tk.BOTH, expand=True)

# Create a Tkinter Button widget to clear messages
# reset = tk.Button(root, text="Clear", command=clear_msg, bg='#F44336', fg='white', borderwidth=0, font=("default", 12))
# reset.pack(side=tk.LEFT, padx=20, pady=(0, 20), fill=tk.BOTH)

# Start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_msg)
receive_thread.start()

root.mainloop()