from email import message
import socket
import time
import json
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def tstap():
    curr_time = datetime.datetime.now()
    time_st = curr_time.timestamp()
    date_time = datetime.datetime.fromtimestamp(time_st)
    str_date_time = date_time.strftime("%H:%M:%S")
    return str_date_time


x = {"id":"s1", "temp":20}
str_x = json.dumps(x)
s.connect(('192.168.123.117', 15000))

#Keep Track of Connection status
connected = True
print("Connected to Server")
message = s.recv(1024).decode("utf-8")

while True:
    #attempt to send and receive data, otherwise reconnect
    try:
        s.send(bytes(str_x, "utf-8"))
        print("Packet sent at {}".format(tstap())) #Printing Time at which data is sent
        message = s.recv(1024).decode("UTF-8")
        print(message)
        time.sleep(15)
    except socket.error:
        #Set Connection status and recreate socket
        connected = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("connection lost..... reconnecting")
        while not connected:
            #Attempt to reconnect, otherwise sleep for 2 seconds
            try:
                s.connect(('192.168.123.117', 15000))
                connected = True
                print("re-connection successful")
            except socket.error:
                time.sleep(2)
  

s.close();
