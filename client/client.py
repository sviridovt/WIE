import socket

HOST = '127.0.0.1'
PORT = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(str.encode('Hello, world'))
data = s.recv(1024)
s.close()
print ('Received', data.decode())
