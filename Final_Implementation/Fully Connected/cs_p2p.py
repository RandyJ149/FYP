import socket
import threading
from _thread import *
from queue import LifoQueue
from urllib import response
import pandas as pd
import joblib
import json
import time
import datetime


server_id = '192.168.53.7'
client_1 = '192.168.123.117'
client_2 = '192.168.123.117'
client_3 = '192.168.123.117'
rtc_device = SDL_DS3231.SDL_DS3231(twi=1, addr=0x68, at24c32_addr=0x57)
#Declaring the Stacks as Global Variable
s1 = LifoQueue()
s2 = LifoQueue()
s3 = LifoQueue()
s4 = LifoQueue()
votes = LifoQueue()

# #Code for testing
# s1.put(20)
# s1.put(15)
# s1.put(20)
# s1.put(21)
# s2.put(20)
# s2.put(21)
# s2.put(15)
# s2.put(21)
# s3.put(21)
# s3.put(20)
# s3.put(20)
# s3.put(20)
# s4.put(20)
# s4.put(21)
# s4.put(21)
# s4.put(16)

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





class Networking(threading.Thread):
    def run(self):
        #Declaring the stacks as Global for uploading Data
        global s1, s2, s3, s4
        ThreadCount = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def AnoMad():
            global s1, s2, s3, s4
            test = joblib.load('rf_4.pkl')

            #Test Code
            # df1 = [[1337, 20, 10.76, 21, 20.03]]
            # df = pd.DataFrame(df1)

            while True:
                start_time = time.time()
                x1, x2, x3, x4 = s1.get(), s2.get(), s3.get(), 20 #20 is the point where DS3231 i2c data is pulled
                df1 = [[1337, x1, x2, x3, x4]]
            #   df1 = [[1337, s1.get(), s2.get(), s3.get(), s4.get()]]
                df = pd.DataFrame(df1)

                x = test.predict(df)
                print(x)
                if(int(x[0])==0):
                    An = "No Anomaly"
                else:
                    An = "Anomaly in Sensor " + str(x[0])
                print("---> Data is [{}, {}, {}, {}] and {} <---".format(x1, x2, x3, x4, An))
                print(time.time() - start_time)
                

        start_new_thread(AnoMad, ())


        try:
            s.bind((server_id, 15000))
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')

        s.listen(10)

        def multi_threaded_client(connection):
#           connection.send(str.encode("Server is working: "))
            connection.send(bytes("Server is waiting for Data", "utf-8"))
            while True:
                data = connection.recv(2048).decode("utf-8")
                data = json.loads(data)
                text = str("Received Data:{} at {} from {}".format(data["temp"], tstap(), data["id"]))
                print(text)
                connection.send(bytes(text, "utf-8"))
                if not data:
                    break
                #Storing Directly into stack using eval()
                eval(data["id"]).put(data["temp"])
            connection.close()

        while True:
            clientsocket, address = s.accept()
            print('Connected to ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (clientsocket, ))
            ThreadCount += 1
            print('Thread Number:' + str(ThreadCount))
        s.close()

#Start of Client Code

class Client(threading.Thread):
    def run(self):

        def multiclient(ip):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Insert Code
            #s.connect((ip, 15000))

            tick = 1

            while tick:
                try:
                    s.connect((ip, 15000))
                    tick = 0
                    time.sleep(15)
                except:
                    time.sleep(2)

            #End of Insert Code

            #Keep Track of Connection status
            connected = True
            print("Connected to Server: {}".format(ip))
            message = s.recv(1024).decode("utf-8")

            while True:
                while ((sync()%30)==0):
                    #attempt to send and receive data, otherwise reconnect
                    try:
                        x = {"id":"s4", "temp":float(rtc_device.getTemp())}
                        str_x = json.dumps(x)
                        s.send(bytes(str_x, "utf-8"))
                        print("Packet sent at {}".format(tstap())) #Printing Time at which data is sent
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
                                s.connect((ip, 15000))
                                connected = True
                                print("re-connection successful")
                            except socket.error:
                                time.sleep(2)
            

            s.close();

        start_new_thread(multiclient, (client_1, ))
        print("Thread 1")
        start_new_thread(multiclient, (client_2, ))
        print("Thread 2")
        start_new_thread(multiclient, (client_3, ))
        print("Thread 3")

        #Code Runner for the time being
        while True:
            print("Code Runner")
            time.sleep(15)
        









t1 = Networking()
c1 = Client()


t1.start()
c1.start()
