import socket
import threading

hostname = socket.gethostname()
host     = socket.gethostbyname(hostname)
port     = 8000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host,port))
print(client_socket)

def msg():
    message = input()
    while message.lower().strip() != "quit":
        client_socket.send(message.encode())
        message = input()
    client_socket.close()

msg_thread        = threading.Thread(target=msg)
msg_thread.daemon = True
msg_thread.start()

while True:
    data = client_socket.recv(1024).decode()
    print(data)