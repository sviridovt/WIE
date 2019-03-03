# allows to import RSA lib from different dir
import sys

# inserts path to access RSA encryption lib
sys.path.insert(0, '../RSAEncryption')

import socket
from RSAKeys import genKeyPair
from RSAKeys import encrypt, decrypt
from RSAKeys import printEncryptedString
from RSAKeys import readPublicKey, readPrivateKey

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
pubKey = readPublicKey()
priKey = readPrivateKey()

certificate = 'starbucks'

# generate RSA key pair
# if files exist dont generate
if pubKey is None or priKey is None:
  if printDebug:
    print('Generating public and private key')
  genKeyPair()
  pubKey = readPublicKey()
  priKey = readPrivateKey()
else:
  if printDebug:
    print('Private and public key files found')

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
if printDebug:
  print('\nRecieved the following message:')
  print('--------------------------------------------------------------------------------\n')
  print(readData(conn))

# TODO send server-pub-key to CA to be signed
# TODO recieve the signed server-pub-key
# TODO send signed server-pub-key to client

# send unsigned public key to client
conn.send(pubKey.encode('utf-8'))

# conn.send(certificate.encode('utf-8'))

# decrypt message
encrypted = conn.recv(2048)
if printDebug:
  print('\nRecieved the following encrypted message:')
  print('--------------------------------------------------------------------------------\n')
  printEncryptedString(encrypted)

decrypted = decrypt(encrypted, priKey, False)

if printDebug:
  print('\nMessage contents after decreption')
  print('--------------------------------------------------------------------------------\n')
  print(decrypted)

"""
# send certificate
# conn.send(certificate.encode('utf-8'))

# read if acknowledged
print('Recieved', readData(conn))

while True:
	data = conn.recv(1024).decode('utf-8')
	if not data: break
	print('Recieved', data)
	conn.send(data)



"""
conn.close()
