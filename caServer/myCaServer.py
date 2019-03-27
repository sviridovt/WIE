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

certificate = 'startbucks'

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
  # keeps track of the entire packet contents
  packet = ''
  # keeps track of the total message size
  recvd = 0

  while true:
    # recieves a message of size 512
    mess = conn.recv(512).decode('utf-8')
    # appends the message to packet
    packet += mess
    # appends the size of the message recieved
    recvd += len(mess)
    # if the message size is less than 512 break
    if len(mess) < 512:
        packet += mess
        break
  if printDebug:
    print('readData:')
    print('message length =', recvd)
    print('message contents')
    print('------------------------------')
    print(packet)
  return packet

def sendData(conn, message):
  if printDebug:
    print('sendData:')
    print('message length =', len(message))
    print('message contents')
    print('------------------------------')
    print(message)

  # iterate through the entire size of the string
  while true:
    # if the message is less than 512 just send it
    if len(message) < 512:
      conn.send(message.encode('utf-8')
      break
    # if its not, sed substring and delete the substring from message
    else:
      submess = message[0:512]
      conn.send(submess.encode('utf-8'))
      # remove substring from message
      message.replace(submess, '', 1)

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
# clientPubKey = conn.recv(1024).decode('utf-8')
clientPubKey = readData(conn)
if printDebug:
  print('\nRecieved the following client public key')
  print('--------------------------------------------------------------------------------\n')
  print(clientPubKey, end='\n\n')

# send encrypted certificate
sendEncrypted(conn, certificate, clientPubKey)

# recieve encrypted message
recvEncrypted(conn, priKey)

conn.close()
