# allows to import libs from different dir
import sys, os

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from hashSignVerify import hashFile, createSig, verifySig
from encDec import encFile, decFile

from EncryptedServerSocket import EncryptedServerSocket
# import the client socket to talk to the caServer
from EncryptedSocket import EncryptedSocket
from libs.RSAKeys import genKeyPair
# from RSAKeys import encrypt, decrypt
# from RSAKeys import printEncryptedString
from libs.RSAKeys import readPublicKey, readPrivateKey
from getSert import renewCert
from datetime import datetime, timedelta
import json

HOST = '127.0.0.1'
PORT = 4443
printDebug = True
certFile = 'cert.txt'

getCert = False

pubKey = readPublicKey()
priKey = readPrivateKey()

SSID = "SecureCanes"

# generate RSA key pair
# if files exist dont generate
if pubKey is None or priKey is None:
  if printDebug:
    print('Generating public and private key')
  genKeyPair()
  pubKey = readPublicKey()
  priKey = readPrivateKey()
  getCert = True
else:
  if printDebug:
    print('Private and public key files found')

if os.path.exists(certFile) and not getCert:
    fl = open(certFile, 'r')
    cert = json.load(fl)
    expiry = datetime.strptime(cert['expiration'], '%Y-%m-%d')
    if expiry <= datetime.now() - timedelta(days=10):
        print(datetime.now() - timedelta(days=10))
        renewCert(pubKey, SSID)
        fl = open(certFile, 'r')
        cert = json.load(fl)
else:
    renewCert(pubKey, SSID)
    fl = open(certFile, 'r')
    cert = json.load(fl)




# open communication with the caServer to obtain certificate
# eSocket = EncryptedSocket(HOST, PORT)

# store the certificate in the given file
# eSocket.storeInFile(certFile)

# close the connection between the caServer
# eSocket.close()

# open server for communication with client
eSocket = EncryptedServerSocket(HOST, PORT)

# send encrypted certificate
eSocket.sendFile(certFile)

# recieve encrypted message
eSocket.storeInFile('response.txt')

#-------------------------------------------------
passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 16 #1024  #512? would have to change enc/dec functions as well

krFname = "privKey.pem"
theirData = ""
#bytes(dataDec)
dataDec = ""

password = "bye"

#create keys (already done by other RSA function in another file)
#krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

while True:
  #server receives 1st
  while eSocket.socket.recv_into(bytearray(bytes(theirData, "utf8"))) > 0: #bytearray(theirData) = eSocket.socket.recv(blocksize):
    dataDec += decFile(theirData, blocksize, ivval, key)
    #will it always be 1024 because of padder?
    print(dataDec)

  #server sends 2nd
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        # \/ 1023?
    key, data = encFile(mydata[num:num+blocksize], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(data, krFname, password, blocksize)  #pass in krFname in sig file from RSA encryption

    num += blocksize

    eSocket.socket.send(key)
  else:
    key, data = encFile(mydata[num:num+length], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(data, krFname, password, blocksize)

    num += length

    eSocket.socket.send(key)

  #-------------------------------------------

# close connection with client
eSocket.close()

