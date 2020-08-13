import tkinter as tk
import socket
import threading


win = tk.Tk()
win.title("Server Management Interface")


# Design all frames:
# - Top Frame: includes the Start and Stop buttons for quick server actions.
# - Middle Frame: includes the Host and Port values of the server.
# - Client List Frame: includes the clients list.


###### TOP FRAME START ######
topFrame = tk.Frame(win)

startBtn = tk.Button(topFrame, text='Start Server', command=lambda : start_server())
startBtn.pack(side=tk.LEFT)

stopBtn = tk.Button(topFrame, text='Stop', command=lambda : stop_server(), state=tk.DISABLED)
stopBtn.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP, pady=(5, 0))
###### TOP FRAME END ######


###### MIDDLE FRAME START ######
middleFrame = tk.Frame(win)

hostLbl = tk.Label(middleFrame, text='Host: X.X.X.X')
hostLbl.pack(side=tk.LEFT)

portLbl = tk.Label(middleFrame, text='Port: XXXX')
portLbl.pack(side=tk.LEFT)

middleFrame.pack(side=tk.TOP, pady=(5, 0))
###### MIDDLE FRAME END ######



###### CLIENT LIST FRAME START ######
clientListFrame = tk.Frame(win)

lineLbl = tk.Label(clientListFrame, text='          CLIENT LIST          ').pack()

scrollbar = tk.Scrollbar(clientListFrame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listDisp = tk.Text(clientListFrame, height=15, width=40)
listDisp.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

# TEST USERS
listDisp.insert(tk.END, "User 1\n")
listDisp.insert(tk.END, "User 1\n")
listDisp.insert(tk.END, "User 1\n")

scrollbar.config(command=listDisp.yview)

listDisp.config(
	yscrollcommand=scrollbar.set,
	background='#F4F6F7',
	highlightbackground='grey',
	state='disabled'
)

clientListFrame.pack(side=tk.BOTTOM, pady=(5, 10))
###### CLIENT LIST FRAME END ######



###### SERVER DATA ######

# Server variables
HOST_ADDR = '127.0.0.1'
HOST_PORT = 4444
BUFSIZE = 4096

# Clients and nicknames list
nick = ' '
clients = []
nicks = []



###### SERVER FUNCTIONS ######

# Start server function
# The code works without the global declaration as well.
def start_server():
	global sv, HOST_ADDR, HOST_PORT

	# UI
	startBtn.config(state=tk.DISABLED)
	stopBtn.config(state=tk.NORMAL)

	# Network
	sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sv.bind((HOST_ADDR, HOST_PORT))
	sv.listen(5)

	threading._start_new_thread(accept_clients, (sv, " "))

	hostLbl['text'] = f"Host: {HOST_ADDR}"
	portLbl['text'] = f"Port: {HOST_PORT}"


def stop_server():
	startBtn.config(state=tk.NORMAL)
	stopBtn.config(state=tk.DISABLED)



# Accept new connections
def accept_clients(server, y):
	while True:
		client, addr = server.accept()
		clients.append(client)

		threading._start_new_thread(send_and_recv_client_msg, (client, addr))

# Function that receives messages from clients then
# broadcasts them to the other clients.
def send_and_recv_client_msg(client_conn, client_ip_addr):
	global sv, nick, clients

	client_msg = ' '

	# Welcome message
	nick = client_conn.recv(BUFSIZE)
	client_conn.send(f"Welcome {nick}! You can use 'exit' to quit the chatroom.".encode())

	nicks.append(nick)

	# Update the list of users connected
	update_client_list(nicks)

	# Start a while loop in which you send and receive messages until a client wants to
	# exit the chatroom.
	while True:
		data = client_conn.recv(BUFSIZE)

		if not data: break
		if data == 'exit': break

		client_msg = data

		idx = get_client_index(clients, client_conn)

		queued_nick = nicks[idx]

		for c in clients:
			if c != client_conn:
				c.send(f"{queued_nick}: {client_msg}")
		

	idx = get_client_index(clients, client_conn)

	# Delete the client's name and IP from the 2 lists.
	del nicks[idx]
	del clients[idx]

	# Close the client connection
	client_conn.close()

	# Update the list of users connected
	update_client_list(nicks)


# Helper function to help get the index of the current client more easily.
def get_client_index(client_list, curr_client):
	idx = 0

	for conn in client_list:
		if conn == curr_client:
			break
		idx += 1

	return idx

def update_client_list(nick_list):
	listDisp.config(state=tk.NORMAL)
	listDisp.delete('1.0', tk.END)

	for c in nick_list:
		listDisp.insert(tk.END, f"{c}\n")
	listDisp.config(state=tk.DISABLED)


# Main loop so the window doesn't disappear.
win.mainloop()