import socket
import json

certFile = 'certificates.json'
HOST = '127.0.0.1'
PORT = 4444

# read database of certificates
with open(certFile, 'r') as fin:
	certificates = json.load(fin)
# make sure that file exists
if certificates is None :
	raise ValueError()

# init  socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host on a given port
s.connect((HOST, PORT))

# send ping request
s.send(str.encode('ping'))

# read recieved data
certificate = s.recv(1024)

# try to find certificate in certificates
try:
	value = certificates[certificate.decode('utf-8')]
	print(certificate.decode('utf-8'), value)
	s.send(str.encode('Acknowledged'))
# if value not found notify user
except KeyError:
	print('certificate not found')
	s.send(str.encode('Go awway!'))

# close socket
s.close()

