from email import message
from http import client
import socket
import time
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


x = {"id":"s1", "temp":20}
str_x = json.dumps(x)
s.connect(('192.168.71.117', 15000))

#Keep Track of Connection status
connected = True
print("connected to server")
message = s.recv(1024).decode("utf-8")

while True:
    #attempt to send and receive data, otherwise reconnect
    try:
        s.send(bytes(str_x, "utf-8"))
        message = s.recv(1024).decode("UTF-8")
        print(message)
        time.sleep(5)
    except socket.error:
        #Set Connection status and recreate socket
        connected = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connection lost..... reconnecting")
        while not connected:
            #Attempt to reconnect, otherwise sleep for 2 seconds
            try:
                s.connect(('192.168.23.117', 9999))
                connected = True
                print("re-connection successful")
            except socket.error:
                time.sleep(2)
  

s.close();
