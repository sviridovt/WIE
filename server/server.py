# allows to import RSA lib from different dir
import sys

# inserts path to access RSA encryption lib
sys.path.insert(0, '../RSAEncryption')

import socket
from RSAKeys import genKeyPair
from RSAKeys import encrypt, decrypt
from RSAKeys import printEncryptedString
from RSAKeys import readPublicKey, readPrivateKey
from RSAKeys import sendEncrypted, recvEncrypted

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
pubKey = readPublicKey()
priKey = readPrivateKey()
clientPubKey = None

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

if printDebug:
  print('\nSending the following server public key:')
  print('--------------------------------------------------------------------------------\n')
  print(pubKey, end='\n\n')

# send unsigned public key to client
conn.send(pubKey.encode('utf-8'))

# recieve the public key from the client
clientPubKey = conn.recv(1024).decode('utf-8')
if printDebug:
  print('\nRecieved the following client public key')
  print('--------------------------------------------------------------------------------\n')
  print(clientPubKey, end='\n\n')

# send encrypted message
sendEncrypted(conn, 'got it!', clientPubKey)

# recieve encrypted message
recvEncrypted(conn, priKey)

conn.close()
