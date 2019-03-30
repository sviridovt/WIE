# allows to import libs from different dir
import sys

# inserts path to access all the libs
sys.path.insert(0, '../libs')

from EncryptedServerSocket import EncryptedServerSocket

HOST = '127.0.0.1'
PORT = 4444
printDebug = True

certificate = 'startbucks'

# open server for communication
eSocket = EncryptedServerSocket(HOST, PORT)

# send encrypted certificate
eSocket.sendFile('certificate.txt')

# recieve encrypted message
eSocket.storeInFile('response.txt')


# TODO send server-pub-key to CA to be signed
# TODO recieve the signed server-pub-key
# TODO send signed server-pub-key to client

# close socket
eSocket.close()
