import socket
import time
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


x = {"id":"s2", "temp":20}
str_x = json.dumps(x)
s.connect(('192.168.23.117', 9999))


while True:
    start_time = time.time()
    # s.connect(('192.168.23.117', 9999))
    print(s)
    s.send(bytes(str_x,"utf-8"))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    # # s.close()
    # time.sleep(10 - (time.time() - start_time))
    time.sleep(0.1)
