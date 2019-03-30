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


# close connection with client
eSocket.close()

