from dataclasses import dataclass
import socket
from threading import *
from queue import LifoQueue
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



class Networking(Thread):
	def run(self):
		#Declaring the stacks as Global for uploading Data
		global s1, s2, s3, s4 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('192.168.50.166', 9999))
		s.listen(5)

		while True:
		clientsocket, address = s.accept()
		data = clientsocket.recv(1024).decode("utf-8")

		data = json.loads(data)
		#Storing Directly into stack using eval()
		eval(data["id"]).put(data["temp"])
		clientsocket.send(bytes("The server received the data", "utf-8"))


		

		

		#Old way of communication for testing
		# name = clientsocket.recv(1024).decode("utf-8")
		# name
		# print(f"Connection from {address} has been established!")
		# clientsocket.send(bytes("Welcome to the Server", "utf-8"))
		clientsocket.close()


class AnoMad(Thread):
	def run(self):
		global s1, s2, s3, s4
		test = joblib.load('model.pkl')

		#Test Code
		# df1 = [[1337, 20, 10.76, 21, 20.03]]
		# df = pd.DataFrame(df1)

		while True:
			start_time = time.time()
			df1 = [[s1.get(), s2.get(), s3.get(), s4.get()]]
			df = pd.DataFrame(df1)

			x = test.predict(df)
			print(x)
			time.sleep(10000 - ((time.time() - start_time)*1000))



