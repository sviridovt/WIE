import socket
from RSAKeys import genKeyPair
from RSAKeys import encrypt, decrypt

HOST = '127.0.0.1'
PORT = 4444
certificate = 'starbucks '

# generate RSA key pair
# if files exist dont generate
# TODO make it so that the keys expire
genKeyPair()

# init socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind to the host and the port
s.bind((HOST, PORT))

# setting a back long for data size
s.listen()

# accepting incomming connection
conn, addr = s.accept()

# printing connected address
print('Connected by', addr)

# reading all of the data from the socket
def readData(conn):
	data = conn.recv(1024).decode('utf-8')
	if not data:
		conn.close()
		raise ValueError()
	return data

# recieve ping request
print('Recieved', readData(conn))

# read public key
with open("pubKey.pem") as f:
        pubKey = f.read()


# TODO send server-pub-key to CA to be signed
# TODO recieve the signed server-pub-key
# TODO send signed server-pub-key to client

# send unsigned public key to client
conn.send(pubKey.encode('utf-8'))

conn.send(certificate.encode('utf-8'))

# decrypt message
encrypted = conn.recv(1024)
print(encrypted)
with open('privKey.pem', 'r') as f:
	privKey = f.read()
	decrypted = decrypt(encrypted, privKey, False)
print(decrypted)


# send certificate
# conn.send(certificate.encode('utf-8'))

# read if acknowledged
print('Recieved', readData(conn))

while True:
	data = conn.recv(1024).decode('utf-8')
	if not data: break
	print('Recieved', data)
	conn.send(data)




conn.close()
