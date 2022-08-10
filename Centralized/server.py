from dataclasses import dataclass
import socket
#from threading import *
from _thread import *
from queue import LifoQueue
from urllib import response
import pandas as pd
import sklearn
import joblib
import json
import time


#Declaring the Stacks as Global Variable
s1 = LifoQueue()
s2 = LifoQueue()
s3 = LifoQueue()
s4 = LifoQueue()

#Code for testing
s1.put(20)
s1.put(15)
s1.put(20)
s1.put(21)
s2.put(20)
s2.put(21)
s2.put(15)
s2.put(21)
s3.put(21)
s3.put(20)
s3.put(20)
s3.put(20)
s4.put(20)
s4.put(21)
s4.put(21)
s4.put(16)



class Networking():
	def start(self):
		#Declaring the stacks as Global for uploading Data
		global s1, s2, s3, s4
		ThreadCount = 0
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		def AnoMad():
			global s1, s2, s3, s4
			test = joblib.load('rf.pkl')

			#Test Code
			# df1 = [[1337, 20, 10.76, 21, 20.03]]
			# df = pd.DataFrame(df1)

			while True:
			#	start_time = time.time()
				df1 = [[1337, s1.get(), s2.get(), s3.get(), s4.get()]]
				df = pd.DataFrame(df1)

				x = test.predict(df)
				print(x)
			#	time.sleep(10 - (time.time() - start_time))

		start_new_thread(AnoMad, ())


		try:
			s.bind(('192.168.71.117', 15000))
		except socket.error as e:
			print(str(e))
		print('Socket is listening..')

		s.listen(10)

		def multi_threaded_client(connection):
#			connection.send(str.encode("Server is working: "))
			connection.send(bytes("Server is working: ", "utf-8"))
			while True:
				data = connection.recv(2048).decode("utf-8")
				connection.send(bytes("Received Data:", "utf-8"))
				if not data:
					break
				data = json.loads(data)
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




t1 = Networking()
t1.start()
