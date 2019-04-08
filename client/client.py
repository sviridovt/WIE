# allows to import RSA lib from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')
#sys.path.insert(0, 'WIE/libs/EncryptedSocket')

#from libs.EncryptedSocket 
import EncryptedSocket
from verify import verify

HOST = '127.0.0.1'
PORT = 4443
printDebug = True

certFile = 'certificates.json'

# read database of certificates
# certificates = Certificates(certFile)

# connect to the server
eSocket = EncryptedSocket.EncryptedSocket(HOST, PORT)

# read the certificate from the server
cert = eSocket.read()

if printDebug:
  print(cert)

# try to find certificate in certificates
if verify(cert):
  # send encrypted message
  eSocket.send('So now what?!')
else:
  # send encrypted message
  eSocket.send('Go away!')

"""
#-------------------------------------------------
passwd = os.urandom(16)
ivval = os.urandom(16)
salt = os.urandom(16)
blocksize = 1024  #512? would have to change enc/dec functions as well

krFname = "privKey.pem"
theirData
bytes(dataDec)

#create keys (already done by other RSA function in another file)
#krFname, kuFname = keyGenerate(password)   #change file names of keys & pass into function?

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
    sig = createSig(fnameDataEnc, sigFname, krFname, password)  #pass in krFname in sig file from RSA encryption

    num += blocksize

    eSocket.socket.send(key)
  else:
    key = encFile(mydata[num:num+length], blocksize, passwd, ivval, salt) #change password/ivval (userinput?)

    #read file2 and hash and sign
    sig = createSig(fnameDataEnc, sigFname, krFname, password)

    num += length

    eSocket.socket.send(key)

  #client receives 2nd
  while bytearray(theirData) = eSocket.socket.recv(blocksize):
    dataDec += decFile(theirData, blocksize, ivval, key)
    #will it always be 1024 because of padder?
    print(dataDec)

  #-------------------------------------------
"""
# close socket
eSocket.close()

