from datetime import datetime

def client_message(client, data):
	client.socket.send(bytes(data, encoding="utf-8"))

def broadcast_message(clients, data):
	for client in clients:
		client_message(client, data)

def broadcast_message_except(clients, data, exclude):
	for client in clients:
		if client == exclude: continue
		client_message(client, data)

def spacer(n):
	return "-" * n

def get_client(clients, name):
	for client in clients:
		if client.name == name:
			return client
	return None

def time_format():
	now = datetime.now()
	return now.strftime("%H:%M:%S")

def nowtime_format():
	now = datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")