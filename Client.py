import socket
import threading
import customtkinter
import tkinter as tk
import datetime
import time
from tkinter import *

root = tk.Tk() # Create a Tkinter form object
root.title("TCP - IP Chat App") # Determine the title of the Tkinter form object
root.geometry('800x600') # Determine the window size of the Tkinter form object
root.configure(bg='#212121') # Determine the background of the Tkinter form object

# Create a Tkinter Listbox widget to display received messages
messageBox = tk.Listbox(root, width=80, height=15, bg='#303030', fg='white', borderwidth=0, font=("default", 15))
messageBox.pack(padx=20, pady=(20, 0), fill=tk.BOTH, expand=True)

# Create a Tkinter Entry widget for the user to enter messages
entry = customtkinter.CTkEntry(master=root,width=500,corner_radius=8)
entry.pack(side=tk.LEFT, padx=(20, 0), pady=(10, 10), fill=tk.BOTH, expand=True)

PORT = 4545 # Listening port
SERVER = socket.gethostbyname(socket.gethostname()) # Get the IP address of the local machine for debugging
SERVER = '26.40.110.128' # Get the IP address of the your server machine

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
    messageBox.delete(0, 'end') # Clear the messages

# Function to find the number of messages
def count():
    counter = 0 # Create variable for message count
    while True:
        # Works until end of messagebox
        if messageBox.get(counter) != '':
            counter = counter + 1 # Increases the variable's value by 1
        else:
            break # It stops when it reaches the end of the messagebox
    return counter # Return variable's value

# Function to backup the messages
def backup_msg():
    time = datetime.datetime.now() # Find the current time
    today = str(datetime.date.today()) # Find the today date
    file_name = "backup-" + today + time.strftime("-%H-%M-%S") + ".txt" # Create a file name according to the now time
    file = open(file_name, "w") # Create a file
    for item in range(1, count()):
            file.write(messageBox.get(item) + "\n") # Backup the message
    file.close() # Close the file

# Function to receive messages from the server
def receive_msg():
    m_control = True # Create a variable to display the error message once
    while True:
        try:
            received_msg = client.recv(1024).decode() # Receive a message from the server
            messageBox.insert(tk.END, received_msg) # Add the message to the messageBox widget
            messageBox.see(tk.END) # Scroll down to new message
        except:
            if m_control:
                messageBox.insert(tk.END, "Disconnected from the server!") # If an exception occurs, display an error message in the messageBox widget
                m_control = False # The message is write once

# Bind the "Return" (aka "Enter") key to the send_msg function
entry.bind("<Return>", send_msg)

# Create a CustomTkinter Button widget to send messages
button = customtkinter.CTkButton(master=root,width=50,fg_color='#0078FF',text_color='white',text='Submit',font=("default", 12),hover=False,command=send_msg)
button.pack(side=tk.LEFT, padx=5, pady=(10, 10), fill=tk.BOTH, expand=True)

# Create a CustomTkinter Button widget to clear messages
reset = customtkinter.CTkButton(master=root,width=50,fg_color='#F44336',text_color='white',text='Clear',font=("default", 12),hover=False,command=clear_msg)
reset.pack(side=tk.LEFT, padx=0, pady=(10, 10), fill=tk.BOTH, expand=True)

# Create a CustomTkinter Button widget to backup messages
backup = customtkinter.CTkButton(master=root,width=50,fg_color='#8A2BE2',text_color='white',text='Backup',font=("default", 12),hover=False,command=backup_msg)
backup.pack(side=tk.LEFT, padx=(5,20), pady=(10, 10), fill=tk.BOTH, expand=True)

# Start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_msg)
receive_thread.start()

root.mainloop()
