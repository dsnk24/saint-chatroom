# Saint's Chatroom, chatroom application made in Python

Saint's Chatroom is a program writted entirely in Python, using the Sockets module for the connections and data and the built-in Tkinter module for the GUI.

**INSTRUCTIONS TO RUN:**
It's very easy to run it, the first thing you do is open a CMD or Terminal, if you're on Mac or Linux and navigate to the folder in which you have the `server.py` and `client.py` files. Type `python server.py` and it will automatically start up the server on your local machine. Open 2 new other terminals and do the same thing for `client.py`. 

# Disclaimer
This is designed to all run on the local machine, using the loopback address ( `127.0.0.1` ). This can be easily modified if you want to use a dedicated server: change the IP Address data to your server's data.

# Prerequisites
You will need the following 2 modules to sucessfully run the chatroom:
1) Sockets
2) Tkinter