import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.50.166', 9999))

name = input("Enter the name")
s.send(bytes(name,"utf-8"))

msg = s.recv(1024)
print(msg.decode("utf-8"))
