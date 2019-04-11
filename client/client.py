# allows to import RSA lib from different dir
import sys, json, os

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from hashSignVerify import hashFile, createSig, verifySig
from encDec import enc, encFile, decFile

from RSAKeys import encrypt, decrypt

from EncryptedSocket import EncryptedSocket
from verify import verify

from Crypto.PublicKey import RSA

HOST = '127.0.0.1'
PORT = 4443
printDebug = True

certFile = 'certificates.json'

# read database of certificates
# certificates = Certificates(certFile)

# connect to the server
eSocket = EncryptedSocket(HOST, PORT)

# read the certificate from the server
cert = eSocket.read()

if printDebug:
  print(cert)

cert = json.loads(cert)

if printDebug:
  print(cert)

# try to find certificate in certificates
if verify(cert):
  # send encrypted message
  eSocket.send('So now what?!')
else:
  # send encrypted message
  eSocket.send('Go away!')

#-------------------------------------------------
passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 16  #024  #512? would have to change enc/dec functions as well

krFname = "privKey.pem"
theirData = ""
#bytes(dataDec)
dataDec = ""

password = "hello"

#create keys (already done by other RSA function in another file)
#krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

#client sends key 1st
k = open(krFname, 'r')
prk = RSA.importKey(k.read())
k.close()
key, encryptor, padder, data = enc(passwd, ivval, salt, blocksize)
Key = prk.encrypt(key, 3422)
eSocket.socket.send(Key)

#cleint receives key 2nd
key2 = eSocket.socket.recv(16) #16? 128? something else?
Key2 = decrypt(key, kuFname)

#check if correct


while True:
#client sends first
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        # \/ 1023?
    data = encFile(mydata[num:num+blocksize], encryptor, padder, data) #change password/ivval (userinput?)

    #read file2 and hash and sign
    #sig = createSig(data, krFname, password, blocksize)  #pass in krFname in sig file from RSA encryption
    #veriify???, write key to file?
    num += blocksize

    eSocket.socket.send(data)
  else:
    data = encFile(mydata[num:num+length], encryptor, padder, data) #change password/ivval (userinput?)

    #read file2 and hash and sign
    #sig = createSig(data, krFname, password, blocksize)

    num += length

    eSocket.socket.send(data)

  #client receives 2nd
  while eSocket.socket.recv_into(bytearray(theirData)) > 0: #bytearray(theirData) = eSocket.socket.recv(blocksize):
    dataDec += decFile(theirData, blocksize, ivval, key)
    #will it always be 1024 because of padder?
    print(dataDec)

  #-------------------------------------------

# close socket
eSocket.close()

