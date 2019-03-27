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
# original on line 56
# serverRSAPublicKey = s.recv(1024).decode('utf-8')
# Making read in packets of 512

while true:
    serverRSAPublicKey = s.recv(512).decode('utf-8')
    
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
with open(certFile, 'r') as fin:
  certificates = json.load(fin)
  # make sure that file exists
  if certificates is None :
    raise ValueError()



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


passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 1024

theirData
bytes(dataDec)

#create keys
krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

While True:
#client sends first
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        # \/ 1023?
    key = encFile(mydata[num:num+blocksize], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(fnameDataEnc, sigFname, krFname, password)

    num += blocksize

    s.send(key)
  else:
    key = encFile(mydata[num:num+length], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(fnameDataEnc, sigFname, krFname, password)

    num += length

    s.send(key)

  #clienbt receives 2nd
  while bytearray(theirData) = s.recv(1024):
    dataDec += decFile(theirData, blocksize, ivval, key)
  #will it always be 1024 because of padder?
# close socket
s.close()
