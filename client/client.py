# allows to import RSA lib from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from EncryptedSocket import EncryptedSocket
from Certificates import Certificates

HOST = '127.0.0.1'
PORT = 4444
printDebug = True

certFile = 'certificates.json'

# read database of certificates
certificates = Certificates(certFile)

# connect to the server
eSocket = EncryptedSocket(HOST, PORT)

# read the certificate from the server
cert = eSocket.read()

# try to find certificate in certificates
if certificates.verify(cert):
  # send encrypted message
  eSocket.send('So now what?!')
else:
  # send encrypted message
  eSocket.send('Go away!')

# close socket
eSocket.close()

