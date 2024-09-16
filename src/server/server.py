import socket
import threading
import utils
from commands import exec_help, exec_pm, exec_datetime, exec_listusers

host_name         = socket.gethostname()
host              = socket.gethostbyname(host_name)
port              = 5000
connected_clients = list()
all_clients 	  = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))

def clength():
	return len(connected_clients)

class Client:
	def __init__(self, name, sck):
		self.name   = name
		self.socket = sck
	def to_string(self):
		return f"{self.name};{self.socket}"

class Command:
	def __init__(self, client, name, args):
		self.client = client
		self.name = name
		self.args = args
	def execute(self, clients, handler):
		handler(clients, self.client, self.name, self.args)

def recv():
	client = connected_clients[clength()-1]
	while True:
		try:
			data = client.socket.recv(1024).decode()
			handle_message(client, data)
		except Exception as e:
			print(e) # should change to smth else
			print(f"Connection is closed ({client.to_string()})")
			connected_clients.remove(client)
			utils.broadcast_message(connected_clients, f"{client.name} disconnected. Headcount: {clength()}")
			break

def handle_message(client, msg):
	if msg.startswith("!") and len(msg) > 1:
		handle_cmd(client, msg.replace("!", "", 1))
	else:
		print(f"[{utils.nowtime_format()}] {client.name}: {msg}")
		msg_self = f"[{utils.time_format()}] {client.name} (You): {msg}"
		msg = f"[{utils.time_format()}] {client.name}: {msg}"
		
		utils.broadcast_message_except(connected_clients, msg, client)
		utils.client_message(client, msg_self)

def handle_cmd(client, cmd):
	parts = cmd.split(" ")
	cmd_name = parts[0].replace("!", "", 1)
	cmd_args = parts[1:]

	if cmd_name == "help":
		Command(client, "help", []).execute(connected_clients, exec_help)
	elif cmd_name == "pm":
		Command(client, "pm", cmd_args).execute(connected_clients, exec_pm)
	elif cmd_name == "datetime":
		Command(client, "datetime", []).execute(connected_clients, exec_datetime)
	elif cmd_name == "listusers":
		Command(client, "listusers", []).execute(connected_clients, exec_listusers)
	else:
		utils.client_message(client, "No such command, use !help to see the commands")

def exit_check():
	if input() == "exit": sock.close()

exit_thread = threading.Thread(target=exit_check)
exit_thread.daemon = True
exit_thread.start()

while True:
	sock.listen()
	conn, addr = sock.accept()
	print(f"Connected by {addr} + conn:{conn}")
	
	all_clients = all_clients+1
	new_client = Client("user" + str(all_clients), conn)
	connected_clients.append(new_client)

	utils.broadcast_message_except(connected_clients,f"{new_client.name} joined. Headcount: {clength()}", new_client)
	utils.client_message(new_client,
		f"{utils.spacer(60)}\nWelcome, your name is {new_client.name}. Current headcount is {clength()}.\n{utils.spacer(60)}")

	msg_thread = threading.Thread(target=recv)
	msg_thread.daemon=True
	msg_thread.start()