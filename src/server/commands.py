import utils
from tabulate import tabulate

help_commands = [
	"help",
	"pm <name> <message>",
	"datetime",
	"listusers"
]

def list_commands():
	comms = ""
	for command in help_commands:
		comms = f"{comms}!{command}\n"
	return comms

def exec_help(clients, client, name, args):
	utils.client_message(client, f"\nAvailable commands:\n{list_commands()}")

def exec_pm(clients, client, name, args):
	try_name = args[0]
	recipient = utils.get_client(clients, try_name)
	if not recipient:
		utils.client_message(client, f"No user with the name \"{try_name}\"")
		return
	if len(args[1:]) < 1:
		utils.client_message(client, f"No message, use !help for correct usage")
		return
	utils.client_message(client, f"[{utils.time_format()}] You -> {client.name}: {args_to_msg(args[1:])}")
	utils.client_message(recipient, f"[{utils.time_format()}] {client.name} -> You: {args_to_msg(args[1:])}")
	
	print(f"[{utils.nowtime_format()}] {client.name} -> {recipient.name}: {args_to_msg(args[1:])}")

def exec_datetime(clients, client, name, args):
	utils.client_message(client, "Current date and time is: " + utils.nowtime_format())
	
def list_users(clients, self_client):
	msg = "List of users:\n"

	userdata = list()
	for client in clients:
		is_you = (" (You)" if client.name == self_client.name else "")
		edited_name = f"{client.name}{is_you}"
		userdata.append((edited_name, client.join_time))
	msg = f"{msg}{tabulate(userdata, headers=('Name', 'Join time'))}"
	return msg
	
def exec_listusers(clients, client, name, args):
	utils.client_message(client, list_users(clients, client))

def args_to_msg(args):
	message = ""
	for piece in args: message = message + " " + piece
	return message