import socket
from KeyChain import KeyChain
from communication import sendEncData, readEncData

printDebug = True

# this class defines an encrypted socket for a client
class EncryptedSocket:
  def __init__(self, host, port):
    # this stores the RSA keys for encrypted communication
    self.keyChain = KeyChain()
    # store the host and port
    self.host = host
    self.port = port
    # init the socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to host on the given port
    self.socket.connect((self.host, self.port))
    if printDebug:
      print('connected to host \'', self.host, ' and port \'', self.port,'\'')

    # setup encrypted communication
    # recieve servers public key
    self.keyChain.readPubKey(self.socket)
    # send public key to server
    self.keyChain.sendPubKey(self.socket)

  # close the socket
  def close(self):
    self.socket.close()

  # send encrypted message
  def send(self, message):
    sendEncData(self.socket, message, self.keyChain.externalPubKey)

  # read encrypted message
  def read(self):
    return readEncData(self.socket, self.keyChain.priKey)
