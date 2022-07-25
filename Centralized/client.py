import socket
import time
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


x = {"id":"s1", "temp":20}
str_x = json.dumps(x)


while True:
    start_time = time.time()
    s.connect(('192.168.50.166', 9999))
    s.send(bytes(str_x,"utf-8"))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    s.close()
    time.sleep(10 - (time.time() - start_time))
