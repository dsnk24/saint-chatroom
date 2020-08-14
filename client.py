# Client.py
# Necessary library imports:
import socket
from threading import Thread
import tkinter as tk



###### CLIENT FUNCTIONALITY ######

# Function used to handle receiving of messages.
def receive():
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode('utf-8')
			msg_list.insert(tk.END, msg)

		# Possibly client leaves chatroom.
		except OSError:
			break


# Function used to handle sending of messages.
def send(event=None):
	msg = user_msg.get()
	user_msg.set("")

	client_socket.send(msg.encode('utf-8'))

	if msg == "[quit]":
		client_socket.close()
		win.quit()


# 'Clean up' Function used called when the window is closed.
def on_close():
	user_msg.set("[quit]")
	send()



# GUI Initialization
win = tk.Tk()
win.title("Saint Chatroom")


###### MESSAGE FRAME START ######

# Definitions
msg_frame = tk.Frame(win)

user_msg = tk.StringVar()

scrollbar = tk.Scrollbar(msg_frame)

msg_list = tk.Listbox(
	msg_frame,
	height=15,
	width=50,
	yscrollcommand=scrollbar.set
)

# Packs
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

msg_frame.pack()

###### MESSAGE FRAME END ######



###### ENTRY BOX START ######

entry_box = tk.Entry(win, textvariable=user_msg)
entry_box.bind("<Return>", send)
entry_box.pack()

send_btn = tk.Button(win, text="Send", command=send)
send_btn.pack()

###### ENTRY BOX END ######


win.protocol("WM_DELETE_WINDOW", on_close)



###### SERVER DATA ######
HOST = '127.0.0.1'
PORT = 33000

BUFSIZ = 4096


###### CLIENT INITIALIZATION AND CONNECTION ######
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = Thread(target=receive)
receive_thread.start()


# Put window on mainloop so it doesn't disappear.
win.mainloop()