# allows to import RSA lib from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

import socket
import json
# this is
from KeyChain import KeyChain
from RSAKeys import encrypt, decrypt
from RSAKeys import printEncryptedString
from RSAKeys import sendEncrypted, recvEncrypted


HOST = '127.0.0.1'
PORT = 4444
printDebug = True
recvd = 0
certFile = 'certificates.json'
# this class contains all the public and private keys
# including the external public key
keyChain = KeyChain()

# TODO implement a way to share rsa keys with server

# TODO store actual certificates in a file
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

# recieve clients public key
keyChain.readPubKey(s)
# send public key to client
keyChain.sendPubKey(s)

# once a secure connection is established, we can recieve the certificate

# read database of certificates
with open(certFile, 'r') as fin:
  certificates = json.load(fin)
  # make sure that file exists
  if certificates is None :
    raise ValueError()

# recive the certificate from the server
certificate = recvEncrypted(s, keyChain.priKey)

# try to find certificate in certificates
try:
  value = certificates[certificate]
  # send encrypted message
  sendEncrypted(s, 'So now what?!', keyChain.externalPubKey)

# if value not found notify user
except KeyError:
  print('certificate not found')
  # send encrypted message
  sendEncrypted(s, 'Go away!', keyChain.externalPubKey)

# close socket
s.close()

