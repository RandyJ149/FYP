import socket
#from threading import *
from _thread import *
from queue import LifoQueue
import json
import time
import datetime


#Declaring the Stacks as Global Variable
s1 = LifoQueue()
s2 = LifoQueue()
s3 = LifoQueue()
s4 = LifoQueue()



def tstap():
    curr_time = datetime.datetime.now()
    time_st = curr_time.timestamp()
    date_time = datetime.datetime.fromtimestamp(time_st)
    str_date_time = date_time.strftime("%H:%M:%S")
    return str_date_time




class Networking():
    def start(self):
        #Declaring the stacks as Global for uploading Data
        global s1, s2, s3, s4
        ThreadCount = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def trustman():
            global s1, s2, s3, s4
            lr = 0.01
            ts = [1, 1, 1, 1]
            res = [0, 0, 0, 0]
            while True:
                res1 = [item * (ts[0]/3) for item in s1.get()]
                res2 = [item * (ts[1]/3) for item in s2.get()]
                res3 = [item * (ts[2]/3) for item in s3.get()]
                res4 = [item * (ts[3]/3) for item in s4.get()]
                for i in range(4):
                    res[i] = res1[i] + res2[i] + res3[i] + res4[i]
#                res = (ts[0]*s1.get() + ts[1]*s2.get() + ts[2]*s3.get() + ts[3]*s4.get())/4
#                print("---> Combined Votes with trust included is {} <---".format(res))
                for i in range(4):
                    ts[i] = ((1 - lr) * ts[i]) + (lr * res[i])
                print("New Trust Values of Sensors are: [s1: {:.2f}, s2: {:.2f}, s3: {:.2f}, s4: {:.2f}]".format(ts[0], ts[1], ts[2], ts[3]))



        start_new_thread(trustman, ())


        try:
            s.bind(('192.168.53.7', 15000))
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
                text = str("Received Data at {} from {}".format(tstap(), data["id"]))
                print(text)
                connection.send(bytes(text, "utf-8"))
                if not data:
                    break
            #   data = json.loads(data)
                #Storing Directly into stack using eval()
                eval(data["id"]).put(data["votes"])
            connection.close()

        while True:
            clientsocket, address = s.accept()
            print('Connected to ' + address[0] + ':' + str(address[1]))
            start_new_thread(multi_threaded_client, (clientsocket, ))
            ThreadCount += 1
            print('Thread Number:' + str(ThreadCount))
        s.close()




t1 = Networking()
t1.start()
