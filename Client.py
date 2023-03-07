import socket
import threading
import sys, subprocess
import tkinter as tk

root = tk.Tk() # create a Tkinter window

entry = tk.Entry() # create a Tkinter Entry widget for user input
entry.pack() # add the Entry widget to the window

messageBox = tk.Listbox(root, width=100, height=20) # create a Tkinter messageBox widget to display received messages
messageBox.pack() # add the messageBox widget to the window

PORT = 4545

# SERVER = "26.97.57.231"
SERVER = socket.gethostbyname(socket.gethostname()) # get the IP address of the local machine for debugging

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the client
client.connect((SERVER, PORT)) # connect the client socket to the server socket

def send_msg(event = None):
    msg = entry.get() # get the message entered by the user
    entry.delete(0, "end") # clear the input field
    message = msg.encode('utf-8') # convert the message to bytes
    client.send(message) # send the message to the server


def recieveMsg():
    while(True):
        try:
            recievedMsg = client.recv(1024).decode() # receive a message from the server
            # Add a value to the message box
            messageBox.insert(tk.END, recievedMsg) # display the received message in the messagebox widget

        except:
            messageBox.insert(tk.END, "Disconnected from the server!") # if an exception occurs, display an error message in the messageBox widget

entry.bind("<Return>", send_msg) # bind the "Return" key to the send_msg function

button = tk.Button(text="Submit", command=send_msg) # create a Tkinter Button widget to send the message
button.pack() # add the Button widget to the window

recieveThread = threading.Thread(target=recieveMsg, args=()) # create a thread for receiving messages
recieveThread.start() # start the thread

GUIThread = threading.Thread(target=root.mainloop(), args=()) # create a thread for the GUI
GUIThread.start() # start the thread