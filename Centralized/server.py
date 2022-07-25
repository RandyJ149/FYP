import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.50.166', 9999))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	name = clientsocket.recv(1024).decode("utf-8")
	name
	print(f"Connection from {address} has been established!")
	clientsocket.send(bytes("Welcome to the Server", "utf-8"))
	clientsocket.close()
