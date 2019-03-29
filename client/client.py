# allows to import RSA lib from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

import json
from EncryptedSocket import EncryptedSocket

HOST = '127.0.0.1'
PORT = 4444
printDebug = True

certFile = 'certificates.json'

# TODO store actual certificates in a file
# read database of certificates
with open(certFile, 'r') as fin:
  certificates = json.load(fin)
  # make sure that file exists
  if certificates is None :
    raise ValueError()

# connect to the server
eSocket = EncryptedSocket(HOST, PORT)

# read the certificate from the server
certificate = eSocket.read()

# try to find certificate in certificates
try:
  value = certificates[certificate]
  # send encrypted message
  eSocket.send('So now what?!')

# if value not found notify user
except KeyError:
  print('certificate not found')
  # send encrypted message
  eSocket.send('Go away!')

# close socket
eSocket.close()

