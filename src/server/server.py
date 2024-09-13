import socket
import threading
from datetime import datetime

from isort.core import process

host_name         = socket.gethostname()
host              = socket.gethostbyname(host_name)
port              = 8001
connected_clients = list()

class Client:
	def __init__(self, name, sck):
		self.name   = name
		self.socket = sck
	def to_string(self):
		return f"{self.name};{self.socket}"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

def recv():
	cl = connected_clients[len(connected_clients)-1]
	while True:
		data = cl.socket.recv(1024).decode()
		# i guess this could be a workaround for the problem stated between L34 and 36
		# still testing
		if len(data) == 0:
			print("Connection is closed")
			connected_clients.remove(cl)
			break
		now = datetime.now()
		message = now.strftime("[%Y-%m-%d %H:%M:%S] ") + cl.name + ": " + data
		print(message)
		# should try/catch somewhere the exception to losing the connection to a client
		# because it tries to a packet to a client who is already disconnected,
		# which causes the server to fault
		for client in connected_clients:
			client.socket.send(str(message).encode())

def exit_check():
	if input() == "exit": sock.close()

exit_thread = threading.Thread(target=exit_check)
exit_thread.daemon = True
exit_thread.start()

while True:
	sock.listen()
	conn, addr = sock.accept()
	print(f"Connected by {addr} + conn:{conn}")

	new_client = Client("anon" + str(len(connected_clients) + 1), conn)
	connected_clients.append(new_client)

	msg_thread = threading.Thread(target=recv)
	msg_thread.daemon=True
	msg_thread.start()