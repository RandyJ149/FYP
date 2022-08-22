from email import message
from http import server
import socket
import time
import json
import datetime
import SDL_DS3231


server_id = '192.168.53.7'
rtc_device = SDL_DS3231.SDL_DS3231(twi=1, addr=0x68, at24c32_addr=0x57)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def tstap():
    curr_time = datetime.datetime.now()
    time_st = curr_time.timestamp()
    date_time = datetime.datetime.fromtimestamp(time_st)
    str_date_time = date_time.strftime("%H:%M:%S")
    return str_date_time


def sync():
    curr_time = datetime.datetime.now()
    time_st = curr_time.timestamp()
    date_time = datetime.datetime.fromtimestamp(time_st)
    str_date_time = date_time.strftime("%S")
    return int(str_date_time)



s.connect((server_id, 15000))

#Keep Track of Connection status
connected = True
print("Connected to Server")
message = s.recv(1024).decode("utf-8")

while True:
    #attempt to send and receive data, otherwise reconnect
    while ((sync()%30)==0):
        try:
            x = {"id":"s1", "temp":float(rtc_device.getTemp())}
            str_x = json.dumps(x)
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
                    s.connect((server_id, 15000))
                    connected = True
                    print("re-connection successful")
                except socket.error:
                    time.sleep(2)
  

s.close();
