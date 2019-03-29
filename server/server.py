# allows to import RSA lib from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

import socket
from KeyChain import KeyChain
from RSAKeys import encrypt, decrypt
from RSAKeys import printEncryptedString
from RSAKeys import sendEncrypted, recvEncrypted

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
clientPubKey = None
# stores and handels all the keys
keyChain = KeyChain()

certificate = 'startbucks'

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

# recieve ping request
if printDebug:
  print('\nRecieved the following message:')
  print('--------------------------------------------------------------------------------\n')
  print(conn.recv(512).decode('utf-8'))

# TODO send server-pub-key to CA to be signed
# TODO recieve the signed server-pub-key
# TODO send signed server-pub-key to client

# send public key to client
keyChain.sendPubKey(conn)
# recieve clients public key
keyChain.readPubKey(conn)


# send encrypted certificate
sendEncrypted(conn, certificate, keyChain.externalPubKey)

# recieve encrypted message
recvEncrypted(conn, keyChain.priKey)

conn.close()
