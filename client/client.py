# allows to import RSA lib from different dir
import sys

# inserts path to access RSA encryption lib
sys.path.insert(0, '../RSAEncryption')

import socket
import json
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

certFile = 'certificates.json'

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

# TODO implement a way to share rsa keys with server

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

# read RSA public key from server
serverRSAPublicKey = s.recv(1024).decode('utf-8')

# print recieved certificate
if printDebug:
  print('\nRSA server public key recieved:')
  print('--------------------------------------------------------------------------------\n')
  print(serverRSAPublicKey)
  print()

if printDebug:
  print('\nSending the following client public key:')
  print('--------------------------------------------------------------------------------\n')
  print(pubKey, end='\n\n')

# sending acknowledgment by sending public key
s.send(str.encode(pubKey))

# recive the message from the server
recvEncrypted(s, priKey)

# send encrypted message
sendEncrypted(s, 'So now what?!', serverRSAPublicKey)

# close socket
s.close()

