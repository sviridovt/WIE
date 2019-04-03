# allows to import RSA lib from different dir
import sys

# inserts path to access RSA encryption lib
sys.path.insert(0, '../RSAEncryption')

import socket
import json
from libs.RSAKeys import genKeyPair
# from RSAKeys import encrypt, decrypt
# from RSAKeys import printEncryptedString
from libs.RSAKeys import readPublicKey, readPrivateKey
from libs.communication import sendEncrypted, recvEncrypted

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
pubKey = readPublicKey()
priKey = readPrivateKey()
recvd = 0
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
# with open(certFile, 'r') as fin:
#   certificates = json.load(fin)

# make sure that file exists
# if certificates is None :
#   raise ValueError()

# init  socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host on a given port
s.connect((HOST, PORT))

# send ping request
s.send(str.encode('ping'))

# read RSA public key from server
# original on line 56
# serverRSAPublicKey = s.recv(1024).decode('utf-8')
# Making read in packets of 512
# open file for reading and writing to a file with 'a', appends the new stuff to the end of the file
def readData(conn):
  packetFile = open("packetText.txt", mode = 'a+')
  recvd = 0
  while True:
    mess = conn.recv(512).decode('utf-8')
    if len(mess) < 512:
        packetFile.write(mess)
        break
    recvd += len(mess)
    packetFile.write(mess)
# packetFile.close()
#packetFile = open("packetText.txt", mode = 'r')
  serverData = packetFile.read(recvd)
  return serverData

# sending data
def sendData(conn, data):
  dataFile = open("sendData.txt", mode = 'a+')
  dataFile.write(data)
  while True:
    packet = dataFile.read(512)
    if len(packet) < 512:
      conn.send(packet.encode('utf-8'))
      sent += len(packet)
      dataFile.close()
      break
    sent += len(packet)
    conn.send(packet.encode('utf-8'))
  return sent

serverRSAPublicKey = readData(s)
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

# once a secure connection is established, we can recieve the certificate

# read database of certificates
# with open(certFile, 'r') as fin:
#   certificates = json.load(fin)
#   make sure that file exists
  # if certificates is None :
  #   raise ValueError()



# recive the certificate from the server
certificate = recvEncrypted(s, priKey)


# try to find certificate in certificates
try:
  value = certificates[certificate]
  # send encrypted message
  sendEncrypted(s, 'So now what?!', serverRSAPublicKey)

# if value not found notify user
except KeyError:
  print('certificate not found')
  # send encrypted message
  sendEncrypted(s, 'Go away!', serverRSAPublicKey)

# close socket
s.close()

