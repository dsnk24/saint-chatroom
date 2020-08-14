# Copyright 2020 Tabacaru Eric
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Server script for a multi-threaded chat application, using sockets.

# Server.py
# Necessary library imports.
import socket
from threading import Thread


# Client and IP dicts.
clients = {}
ip_addrs = {}


###### SERVER DATA ######

# Constants
SV_HOST = '127.0.0.1'
SV_PORT = 33000
BUFSIZ = 4096

# Server
sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv.bind((SV_HOST, SV_PORT))



###### SERVER FUNCTIONALITY ######

# Function that accepts new connections to the server.
def accept_connections():
	while True:
		client, addr = sv.accept()

		print(f"New connection from {addr}!")

		client.send(
			"Welcome to Saint's Chatroom! He also goes by the name of dsnk! Please type your nickname and press Enter!".encode('utf-8')
		)

		ip_addrs[client] = addr

		Thread(target=handle_client, args=(client,)).start()


# Function used to handle client messages and connection.
def handle_client(client):
	# First receives the client's name in response to the previous server message.
	name = client.recv(BUFSIZ).decode('utf-8')

	# Send a message about how to properly disconnect from the server.
	greet_msg = f"Nice to meet you {name}! If you ever want to quit the chatroom, type '[quit]'.".encode('utf-8')
	client.send(greet_msg)

	# Broadcast a message informing people that a new person joined the chat.
	broadcast(f"{name} has joined the chat! Everybody give him a warm welcome!".encode('utf-8'))

	clients[client] = name


	# Start of main communication loop. First it stores the message received from the client inside the 'msg' variable,
	# Then it checks if the msg is '[quit]', if true it closes the socket connection to that client and then echos
	# '[quit]' to the client to shut down the client as well. If it's not true, then it simply broadcasts the message
	# to all the clients.
	while True:
		msg = client.recv(BUFSIZ)

		if msg != "[quit]".encode('utf-8'):
			broadcast(msg, f"{name}: ".encode('utf-8'))
		
		else:
			client.send("[quit]".encode('utf-8'))
			client.close()

			del clients[client]

			broadcast(f"{name} has left the chat.".encode('utf-8'))

			break

# Function used to easily send a data packet to all the clients connected on the server.
# Note: Optional argument 'prefix' which is used to let the other users know who sent the message. If none
# is provided, it will simply send the message with no prefix, letting the users know this is a system message.
def broadcast(msg, prefix=" ".encode('utf-8')):
	for client in clients:
		client.send(prefix + msg)



if __name__ == "__main__":
	sv.listen(5)

	print(f"Listening on {SV_HOST}:{SV_PORT}")

	accept_thread = Thread(target=accept_connections)
	accept_thread.start()
	accept_thread.join()

	sv.close()