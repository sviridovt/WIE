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
from cryptography.hazmat.primitives import serialization

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
APPuk = cert['pubKey']
print("public key", APPuk, end='\n\n')
APPuk = RSA.importKey(APPuk)
print('server pubkey\n\n',APPuk,end='\n\n')


# try to find certificate in certificates
if verify(cert):
  # send encrypted message
  eSocket.send('So now what?!')
else:
  # send encrypted message
  eSocket.send('Go away!')
  exit()

#-------------------------------------------------
passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 16  #024  #512? would have to change enc/dec functions as well

krFname = "privKey.pem"
kuFname = "pubKey.pem"
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
#prk
#with open(krFname, 'rb') as file:
#  prk = serialization.load_pem_private_key(
#    data = file.read(),
#    #password = password.encode(),
#    #backend = backend
#  )
#file.close()
#prk = prk[31:-29]
key, encryptor, padder, data = enc(passwd, ivval, salt, blocksize)
print("key \n", key, end="\n\n")

Key = APPuk.encrypt(key, 3422)[0]
print("Key", Key, end="\n\n")
print("has\n", APPuk.has_private(), end="\n\n")

#print(Key)
# eSocket.socket.send(bytes(str(Key), "utf8"))
#print(Key)

eSocket.socket.send(Key,1024)
#print(len(bytes(str(Key), "utf8")))
print("aes key sent with rsa public key")

#cleint receives key 2nd
key2 = eSocket.socket.recv(1024)#read() #socket.recv(16) #16? 128? something else?
#Key2 = decrypt(key2, kuFname)
'''
k = open(kuFname, 'r')
puk = RSA.importKey(k.read())
k.close()
Key2 = puk.decrypt(key2)
'''
print("key2", key2, end="\n\n")
Key2 = prk.decrypt(key2)
#key = RSA.importKey(key)
#decrypt = puk.decrypt(encrypted_message)
print("has\n", prk.has_private(), end="\n\n")
print('key2\n\n',Key2, end='\n')
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

