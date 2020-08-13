import tkinter as tk
from tkinter import messagebox
import socket
import threading


window = tk.Tk()
window.title("Client")


username = " "


###### TOP FRAME START ######
topFrame = tk.Frame(window)

nameLbl = tk.Label(topFrame, text = "Name: ").pack(side=tk.LEFT)

nameEntry = tk.Entry(topFrame)
nameEntry.pack(side=tk.LEFT)

connectBtn = tk.Button(topFrame, text="Connect", command=lambda : connect())
connectBtn.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP)
###### TOP FRAME END ######



###### DISPLAY FRAME START ######
displayFrame = tk.Frame(window)

lineLbl = tk.Label(displayFrame, text="*********************************************************************").pack()

scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

tkDisplay.tag_config("tag_your_message", foreground="blue")

scrollBar.config(command=tkDisplay.yview)

tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")

displayFrame.pack(side=tk.TOP)
###### DISPLAY FRAME END ######



###### BOTTOM FRAME START ######
bottomFrame = tk.Frame(window)

messageBox = tk.Text(bottomFrame, height=2, width=55)
messageBox.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))

messageBox.config(highlightbackground="grey", state="disabled")

messageBox.bind("<Return>", (lambda event: get_chat_msg(tkMessage.get("1.0", tk.END))))

bottomFrame.pack(side=tk.BOTTOM)
###### BOTTOM FRAME END ######



###### CLIENT FUNCTIONALITY ######

# Function used to pass the username data and check if it is valid.
def connect():
	global username, client

	if len(nameEntry.get()) < 1:
		tk.messagebox.showerror(title="Error", message=f"{nameEntry.get()} is not a valid nickname.")

	else:
		username = nameEntry.get()
		connect_to_sv(username)


client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 4444

# Function used to establish a connection to the server.
def connect_to_sv(name):
	global client, HOST_PORT, HOST_ADDR

	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((HOST_ADDR, HOST_PORT))
		client.send(name)

		nameEntry.config(state=tk.DISABLED)
		connectBtn.config(state=tk.DISABLED)
		messageBox.config(state=tk.DISABLED)

		# Start a new thread as to not overwhelm the main one.
		threading._start_new_thread(recv_msg_from_sv, (client, 'm'))

	except:
		tk.messagebox.showerror(title="Error", message=f"Cannot connect to host {HOST_ADDR} on port {HOST_PORT}")


def recv_msg_from_sv(sck, m):
	while True:
		msg_from_sv = sck.recv(4096)

		if not msg_from_sv: break

		# Display message from server on chatroom.

		# Enable the display area, insert text then disable it.

		texts = tkDisplay.get("1.0", tk.END).strip()
		tkDisplay.config(state=tk.NORMAL)

		if len(texts) < 1:
			tkDisplay.insert(tk.END, f"{msg_from_sv}")
		else:
			tkDisplay.insert(tk.END, f"\n\n{msg_from_sv}")

		tkDisplay.config(state=tk.DISABLED)
		tkDisplay.see(tk.END)


	sck.close()
	window.destroy()


def get_chat_msg(msg):
	msg = msg.replace('\n', '')

	texts = tkDisplay.get("1.0", tk.END).strip()

	tkDisplay.config(state=tk.NORMAL)


	if len(texts) < 1:
		tkDisplay.insert(tk.END, f"You: {msg}", "tag_your_message")
	else:
		tkDisplay.insert(tk.END, f"\n\nYou: {msg}", "tag_your_message")


	tkDisplay.config(state=tk.DISABLED)

	send_msg_to_sv(msg)

	tkDisplay.see(tk.END)
	tkMessage.delete('1.0', tk.END)


def send_msg_to_sv(msg):
	client.send(msg)

	if msg == "exit":
		client.close()
		window.destroy()

window.mainloop()