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
	# data = conn.recv(1024).decode('utf-8')
	# if not data:
	# 	conn.close()
	#	raise ValueError()
	# return data
  packetFile = open("packetText.txt", mode = 'r+a')
  while true:
    mess = conn.recv(512).decode('utf-8')
    if len(mess) < 512:
        packetFile.write(mess)
        break
    recvd += len(mess)
    packetFile.write(mess)
# packetFile.close()
#packetFile = open("packetText.txt", mode = 'r')
  clientData = packetFile.read(recvd)
  packetFile.close()
  return clientData

def sendData(conn, data):
  dataFile = open("sendData.txt", mode = 'r+a')
  dataFile.write(data)
  while true:
    packet = dataFile.read(512)
    if len(packet) < 512:
      conn.send(packet.encode('utf-8'))
      sent += len(packet)
      dataFile.close()
      break
    sent += len(packet)
    conn.send(packet.encode('utf-8'))
  return sent


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
