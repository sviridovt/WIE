# allows to import libs from different dir
import sys, os

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from hashSignVerify import hashFile, createSig, verifySig
from encDec import enc, encFile, decFile

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
from Crypto.PublicKey import RSA


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
CPuk = eSocket.keyChain.externalPubKey
CPuk = RSA.importKey(CPuk)

#-------------------------------------------------
passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 16 #1024  #512? would have to change enc/dec functions as well

krFname = "privKey.pem"
kuFname = "pubKey.pem"
theirData = ""
#bytes(dataDec)
dataDec = ""

password = "bye"

#create keys (already done by other RSA function in another file)
#krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

#server receives key 1st
key2 = eSocket.conn.recv(1024)#eSocket.socket.recv(1451)#read() #.socket.recv(1451) #16? 128? something else?
#key2 = eSocket.read()
print('received key\n',key2, end='\n\n')


#Key2 = decrypt(key, kuFname)
k = open(krFname, 'r')
prk = RSA.importKey(k.read())
k.close()
print("has\n", prk.has_private(), end="\n\n")
Key2 = prk.decrypt(key2)
#prk.publickey.decrypt

#check if correct
print('key2\n\n',Key2, end='\n')


#server sends key 2nd
#k = open(krFname, 'r')
#prk = RSA.importKey(k.read())
#k.close()
#prk
#with open(krFname, 'rb') as file:
#  prk = serialization.load_pem_private_key(
#    data = file.read(),
#    #password = password.encode(),
#    #backend = backend
#  )
#file.close()
key, encryptor, padder, iv = enc(passwd, ivval, salt, blocksize)
Key = CPuk.encrypt(key, 3422)[0]
eSocket.conn.send(Key, 1024)#eSocket.socket.send(bytes(str(Key), "utf8"))
print(Key2)
print("has\n", CPuk.has_private(), end="\n\n")

iv2 = eSocket.conn.recv(1024)
print("iv2\n", iv2, end="\n\n")
eSocket.conn.send(iv, 1024)
print("iv sent\n", iv, end="\n\n")
#eSocket.conn.send(salt, 1024)


#r = eSocket.read()
#print('read')
#print(r)

while True:
  #server receives 1st
  theirData = eSocket.conn.recv(blocksize)
  print(theirData)
  while  theirData: #eSocket.conn.recv_into(bytearray(bytes(theirData, "utf8"))) > 0: #bytearray(theirData) = eSocket.socket.recv(blocksize):
    dataDec = decFile(theirData, blocksize, iv2, key) #only do padder.update(salt) first time then save salt for next sends
    #will it always be 1024 because of padder?
    print(dataDec)

  #server sends 2nd
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        # \/ 1023?
    data = encFile(mydata[num:num+blocksize], encryptor, padder, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    #sig = createSig(data, krFname, password, blocksize)  #pass in krFname in sig file from RSA encryption

    num += blocksize

    eSocket.conn.send(data)
  else:
    data = encFile(mydata[num:num+length], encryptor, padder, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    #sig = createSig(data, krFname, password, blocksize)

    num += length

    eSocket.conn.send(data)

  #-------------------------------------------
  
# close connection with client
eSocket.close()

