import socket
import threading
import sys, subprocess
import tkinter as tk

<<<<<<< Updated upstream
root = tk.Tk() # create a Tkinter window
root.title(" TCP - IP Sohbet Programı") # determine the title of the window
root.geometry('400x300') # determine the weight and height of the window
root.configure(bg = '#066595') # determine the background color of the window

messageBox = tk.Listbox(root, width = 60, height = 10) # create a Tkinter messageBox widget to display received messages
messageBox.configure(bg = '#512B58', fg = 'white')
messageBox.pack(expand = True) # add the messageBox widget to the window

entry = tk.Entry() # create a Tkinter Entry widget for user input
entry.configure(bg = '#512B58', fg = 'white')
entry.pack(expand = True) # add the Entry widget to the window
=======
root = tk.Tk()
root.title("TApp")
root.geometry('600x400') # determine the weight and height of the window
root.configure(bg = '#212121') # determine the background color of the window

# create a Tkinter messageBox widget to display received messages 
messageBox = tk.Listbox(root, width = 60, height = 10, bg = '#303030', fg = 'white', borderwidth = 0) 
messageBox.pack(padx = 10, pady = 10, fill = tk.BOTH, expand = True) # add the messageBox widget to the window

entry = tk.Entry(root, bg = '#303030', fg = 'white', borderwidth = 0, font = ("default", 20))
entry.pack(side = tk.LEFT, padx = 10, pady = 10, fill = tk.BOTH, expand = True) # add the Entry widget to the window
>>>>>>> Stashed changes

PORT = 4545

SERVER = socket.gethostbyname(socket.gethostname()) # get the IP address of the local machine for debugging
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the client
client.connect((SERVER, PORT)) # connect the client socket to the server socket

def send_msg(event = None):
    msg = entry.get() # get the message entered by the user
    entry.delete(0, "end") # clear the input field
    message = msg.encode('utf-8') # convert the message to bytes
    client.send(message) # send the message to the server

def clear_msg(event = None):
<<<<<<< Updated upstream
    messageBox.delete(0, 'end')
=======
    messageBox.delete(0, 'end') #Clears messagebox
>>>>>>> Stashed changes

def recieveMsg():
    while(True):
        try:
            recievedMsg = client.recv(1024).decode() # receive a message from the server
            # Add a value to the message box
            messageBox.insert(tk.END, recievedMsg) # display the received message in the messagebox widget
        except:
            messageBox.insert(tk.END, "Disconnected from the server!") # if an exception occurs, display an error message in the messageBox widget

<<<<<<< Updated upstream
entry.bind("<Return>", send_msg) # bind the "Return" key to the send_msg function

button = tk.Button(text="SUBMIT", command=send_msg) # create a Tkinter Button widget to send the message
button.configure(bg = '#60A917', fg = 'white')
button.pack(expand = True) # add the Button widget to the window

reset = tk.Button(text="CLEAR", command=clear_msg) # create a Tkinter Button widget to send the message
reset.configure(bg = '#A20025', fg = 'white')
reset.pack(expand = True) # add the Button widget to the window
=======
# #SUBMIT BUTTON
entry.bind("<Return>", send_msg) # bind the "Return" (aka "Enter") key to the send_msg function
button = tk.Button(root, text = "Submit", command = send_msg, bg = '#4CAF50', fg = 'white', borderwidth = 0) # create a Tkinter Button widget to send the message
button.pack(side = tk.LEFT, padx = 0, pady = 0, fill = tk.BOTH, expand = True) # add the Button widget to the window

# #CLEAR BUTTON
reset = tk.Button(root, text = "Clear", command = clear_msg, bg = '#f44336', fg = 'white', borderwidth = 0)
reset.pack(side = tk.LEFT, padx = 0, pady = 0, fill = tk.BOTH, expand = True)

receive_thread = threading.Thread(target = receive_msg, args = ()) # create a thread for receiving messages
receive_thread.start()
>>>>>>> Stashed changes

recieveThread = threading.Thread(target=recieveMsg, args=()) # create a thread for receiving messages
recieveThread.start() # start the thread

GUIThread = threading.Thread(target=root.mainloop(), args=()) # create a thread for the GUI
GUIThread.start() # start the thread