# allows to import libs from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from EncryptedServerSocket import EncryptedServerSocket
# import the client socket to talk to the caServer
from EncryptedSocket import EncryptedSocket

HOST = '127.0.0.1'
PORT = 4444
printDebug = True
certFile = 'cert.txt'

# open communication with the caServer to obtain certificate
eSocket = EncryptedSocket(HOST, PORT)

# store the certificate in the given file
eSocket.storeInFile(certFile)

# close the connection between the caServer
eSocket.close()

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
blocksize = 1024  #512? would have to change enc/dec functions as well

theirData
bytes(dataDec)

#create keys (already done by other RSA function in another file)
#krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

While True:
#server receives first
  while bytearray(theirData) = eSocket.socket.recv(blocksize):
    dataDec += decFile(theirData, blocksize, ivval, key)
    #will it always be 1024 because of padder?
    print(dataDec)

#server sends second
  mydata = input("Enter data: ")
  if mydata == "end":
    break
  num = 0
  length = len(mydata)
  if length > blocksize:        # \/ 1023?
    key = encFile(mydata[num:num+blocksize], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(fnameDataEnc, sigFname, krFname, password)  #pass in krFname in sig file from RSA encryption

    num += blocksize

    eSocket.socket.send(key)
  else:
    key = encFile(mydata[num:num+length], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(fnameDataEnc, sigFname, krFname, password)

    num += length

    eSocket.socket.send(key)

  #-------------------------------------------

# close connection with client
eSocket.close()
