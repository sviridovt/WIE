import socket
import json
from RSAKeys import genKeyPair
from RSAKeys import encrypt

certFile = 'certificates.json'
HOST = '127.0.0.1'
PORT = 4444

# generate RSA key pair
genKeyPair()

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

# read and print recieved data
certificate = s.recv(1024).decode('utf-8')
print('Certificate recieved', certificate)

# try to find certificate in certificates
try:
	value = certificates[certificate]
	print(certificate.decode('utf-8'), value)
	s.send(str.encode('Acknowledged'))
# if value not found notify user
except KeyError:
	print('certificate not found')
	s.send(str.encode('Go awway!'))

# close socket
s.close()

