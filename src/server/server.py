import socket
import threading
from datetime import datetime

host_name         = socket.gethostname()
host              = socket.gethostbyname(host_name)
port              = 8000
connected_clients = list()
all_clients 	  = 0

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
		try:
			data = cl.socket.recv(1024).decode()
			# i guess this could be a workaround for the problem stated between L34 and 36
			# still testing
			now = datetime.now()
			message = now.strftime("[%Y-%m-%d %H:%M:%S] ") + cl.name + ": " + data
			print(message)
			# should try/catch somewhere the exception to losing the connection to a client
			# because it tries to a packet to a client who is already disconnected,
			# which causes the server to fault
			broadcast_message(message)
		except Exception as e:
			print(f"Connection is closed ({cl.to_string()})")
			connected_clients.remove(cl)
			broadcast_message(f"{cl.name} disconnected. Headcount: {len(connected_clients)}")
			break

def exit_check():
	if input() == "exit": sock.close()

exit_thread = threading.Thread(target=exit_check)
exit_thread.daemon = True
exit_thread.start()

def client_message(client, data):
	client.socket.send(bytes(data, encoding="utf-8"))#.encode()

def broadcast_message(data):
	for client in connected_clients:
		client_message(client, data)

def broadcast_message_except(data, exclient):
	for client in connected_clients:
		if client == exclient: continue
		client_message(client, data)

def spacer(n):
	return "-"*n

while True:
	sock.listen()
	conn, addr = sock.accept()
	print(f"Connected by {addr} + conn:{conn}")

	all_clients = all_clients + 1
	new_client = Client("Anon" + str(all_clients), conn)
	connected_clients.append(new_client)

	broadcast_message_except(f"{new_client.name} joined. Headcount: {len(connected_clients)}", new_client)
	client_message(new_client, f"{spacer(30)}\nWelcome, your name is {new_client.name}. Current headcount is {len(connected_clients)}.\n{spacer(30)}")

	msg_thread = threading.Thread(target=recv)
	msg_thread.daemon=True
	msg_thread.start()